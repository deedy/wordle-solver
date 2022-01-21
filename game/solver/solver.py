from typing import List, Dict, Set, Tuple, Type
from collections import defaultdict, Counter
from ..constants import GUESS_RIGHT_SPOT, DEFAULT_SOLVER_SETTINGS
from ..wordle import Wordle
from .util import is_guessable_word, parse_clues
from ..util import get_n_from_word_set

def solve_wordle(
    wordle: Type[Wordle],
    solver_settings: Dict[str, bool]=DEFAULT_SOLVER_SETTINGS,
    debug: int=1
) -> Tuple[bool, int, List[str]]:
    clues = []
    MAX_GUESSES = int(solver_settings['max_guesses'])
    for i in range(MAX_GUESSES):
        chosen, cands, numcands = guess_next_word(clues, solver_settings=solver_settings, debug=debug)
        if debug >= 1:
            print(f'Choosing [{chosen}]. Total {numcands} candidates: {cands}...')
        clue, state = wordle.guess(chosen)
        if clue:
            clues.append((chosen, clue))
        if state == Wordle.SOLVED:
            if debug >= 1:
                print(f'Woohoo! Solver solved it in {i+1} guesses!')
            return True, i+1, cands
        elif state == Wordle.UNSOLVED:
            if debug >= 1:
                print('Oh no, it beat the solver :(')
            return False, -1, cands

# Returns a tuple of 
# - a chosen next guess
# - a list of possible candidate words left to solve the wordle
# - the number of possible candidate words left
def guess_next_word(
    clues: List[Tuple[str, List[int]]],
    solver_settings: Dict[str, bool]=DEFAULT_SOLVER_SETTINGS,
    debug: int=1,
) -> Tuple[str, List[str], int]:
    if not 'candidate_set' in solver_settings or not len(solver_settings['candidate_set']): 
        raise Exception('candidate_set not specified in config')
    candidates = solver_settings['candidate_set']
    if not 'guess_set' in solver_settings or not len(solver_settings['guess_set']): 
        word_set = solver_settings['candidate_set']
    else:
        word_set = solver_settings['guess_set']

    if 'solution_tree' in solver_settings and len(solver_settings['solution_tree']):
        base = solver_settings['solution_tree']
        for word, clue in clues:
            if not word in base:
                raise Exception('No candidates left! Its possible you\'re not using an accurate solution tree for this configuration!')
            strclue = ''.join(map(str, clue))
            if not strclue in base[word]:
                raise Exception('No candidates left! Its possible you\'re not using an accurate solution tree for this configuration!')
            base = base[word][strclue]
        keys = list(base.keys())
        if len(clues) and len(clues[-1][1])and len(set(clues[-1][1])) == 1 and clues[-1][1][0] == GUESS_RIGHT_SPOT:
            return None, [], 0
        if not len(keys):
            raise Exception('No candidates left! Its possible you\'re not using an accurate solution tree for this configuration!')
        return keys[0], [keys[0]], 1



    N = get_n_from_word_set(word_set)
    MAX_GUESSES = int(solver_settings['max_guesses'])
    NON_POS_WEIGHT = float(solver_settings['non_pos_weight'])
    word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues, debug=debug)
    prev_guesses = set([w for w, _ in clues])
    # Check if the last clue was fully correct
    if len(clues) and len(clues[-1][1]) and is_guessable_word(clues[-1][0], word_right_place, in_word_wrong_place, not_in_word) and len(set(clues[-1][1])) == 1 and clues[-1][1][0] == GUESS_RIGHT_SPOT:
        return None, [], 0

    cands = [w for w in candidates \
            if not w in prev_guesses and is_guessable_word(w, word_right_place, in_word_wrong_place, not_in_word)]
    
    if not len(cands):
        raise Exception('No candidates left! Its possible you\'re not using an accurate dictionary!')
    guess_left = MAX_GUESSES - len(clues)
    # len(cands) <= guess_left (this condition guarantees brute force solving, but takes more attempts)
    if len(cands) == 1 or guess_left == 1: 
        # We can just guess them all individually or don't have enough guesses left
        return cands[0], cands, len(cands)

    # Explore (non-strict candidates) if
    # - we have 3 of the letters right 
    # - more cands than guesses, we go non-strict to reduce the set. 
    # - not last guess
    new_musts = [set() for x in range(N)]
    for ix in range(N):
        for c in cands:
            new_musts[ix].add(c[ix])
    for ix, cond in enumerate(new_musts): 
        if len(cond) == 1:
            letter = list(cond)[0]
            word_right_place[letter].add(ix)
    places_known = set([x for setx in word_right_place.values() for x in setx])
    unknown_places = set([ix for ix in range(N) if not ix in places_known])
    
    # Assemble character frequencies of remaining candidates
    conditional_unknown_freq = defaultdict(int)
    conditional_pos_freq = [defaultdict(int) for i in range(N)]
    total_unknown_freq = 0
    for c in cands:
        for i, l in enumerate(c):
            if not i in unknown_places:
                continue
            if l in not_in_word: # and not i in word_right_place[l]:# and not l in in_word_wrong_place:
                continue
            conditional_unknown_freq[l] += 1
            conditional_pos_freq[i][l] += 1
            total_unknown_freq += 1

    if total_unknown_freq == 0:
        raise Exception(f'No frequency distribution could be attained from remaining {len(cands)} candidates. This should never happen.')
    if not solver_settings['use_pos']:
        def sort_maximal_nonpos(word):
            # Sort by the number of times a character in a word appears
            # globally in any unknown place in the remaining candidate set
            return -sum([conditional_unknown_freq[c] for c in set(word)])
        sortfn = sort_maximal_nonpos
    else:
        def sort_maximal_position_with_nonpos(word, sort=True):
            # Sort by the number of times a character in a word appears
            # in the right position of any unknown place in the word and weigh
            # it with appearances in the wrong place by NON_POS_WEIGHT
            visited = [0 for i in range(26)]
            score, nonpos_score = 0, 0
            for i, c in enumerate(word):
                charix = ord(c)-ord('a')
                if visited[charix]:
                    continue 
                else:
                    visited[charix] = 1
                # += does well also but performs worse for duplicate letters
                score += conditional_pos_freq[i][c]
                nonpos_score += conditional_unknown_freq[c] - conditional_pos_freq[i][c]
                # # += does well also but performs worse for duplicate letters
                # score[charix] = conditional_pos_freq[i][c]
                # nonpos_score[charix] = conditional_unknown_freq[c] - score[charix]
            sortscore = -(score + NON_POS_WEIGHT * nonpos_score)
            if sort:
                return sortscore
            return ([(chr(i + ord('a')), v) for i, v in enumerate(score) if v],
                    [(chr(i + ord('a')), v) for i, v in enumerate(nonpos_score) if v], sortscore)
        sortfn = sort_maximal_position_with_nonpos

    
    explorable = word_set if solver_settings['non_strict'] else cands
    explorable = [cand for cand in explorable if cand not in prev_guesses]
    explorable.sort(key=sortfn)
    max_val = sortfn(explorable[0])
    explorable = [x for x in explorable if sortfn(x) == max_val]

    if len(explorable) > 0:
        # Break ties by boosting words with known letter guesses because
        # they can appear in the word again and need to be explicitly checked for
        # because simply guessing them in the wrong place will always return 🟨 
        # because it exists in the word twice
        # Don't think this is needed for use_pos = true
        def boost_letters_in_right_place(word):
            score = 0
            for i, c in enumerate(word):
                if c in new_musts[i] and len(new_musts[i]) > 1:
                    if c in word_right_place:
                        score += 1
            return -score
        explorable.sort(key=boost_letters_in_right_place)
        max_val2 = boost_letters_in_right_place(explorable[0])
        explorable = [x for x in explorable if boost_letters_in_right_place(x) == max_val2]
    
    if debug >= 2:
        print('Inferred conditions ', [''.join(m) for m in new_musts])
        cond_probs = [(x, y) for x, y in conditional_unknown_freq.items() if y]
        print(f'Conditional ({len(cond_probs)}):{cond_probs}\nCands ({len(cands)}): {cands[:100]}...\n')
        print(f'Explore cands ({len(explorable)}): {[(c, sortfn(c), boost_letters_in_right_place(c)) for c in explorable[:10]]}')

    if not len(explorable):
        raise Exception(f'No more explorable candidates. This should never happen.')
    chosen = min(explorable)
    return chosen, cands[:5], len(cands)
     