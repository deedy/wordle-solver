from typing import List, Dict, Set, Tuple, Type
from collections import defaultdict, Counter
from ..constants import MAX_GUESSES, NOTHING, GUESS_WRONG_SPOT, GUESS_RIGHT_SPOT
from ..wordle import Wordle
from .util import is_guessable_word
from ..util import get_n_from_word_set
	
DEFAULT_SETTINGS = {
	'use_conditional': True,
	'non_strict': True,
	'use_pos': True,
}

def parse_clues(clues: List[Tuple[str, List[int]]], debug=False) -> Tuple[Dict[str, Set[int]], Dict[str, Set[int]], Set[str]]:
	if not len(clues):
		return {}, {}, set()
	N = len(clues[0][0])
	not_in_word = set()
	in_word_wrong_place = defaultdict(set)
	word_right_place = defaultdict(set)
	for w, clue_res in clues:
		for i in range(len(clue_res)):
			if clue_res[i] == NOTHING:
				not_in_word.add(w[i])
			elif clue_res[i] == GUESS_WRONG_SPOT:
				in_word_wrong_place[w[i]].add(i)
			elif clue_res[i] == GUESS_RIGHT_SPOT:
				word_right_place[w[i]].add(i)
			else:
				assert False
	if debug:
		fword = ['_'] * N
		for c, ixes in word_right_place.items():
			for ix in ixes:
				fword[ix] = c
		word_format = ''.join(fword)
		wrong_place = [(x, y) for x, y in in_word_wrong_place.items()]
		not_word = ''.join(not_in_word)
		print(f'Right: [{word_format}] Wrong: {wrong_place} Absent: [{not_word}]')
	return word_right_place, in_word_wrong_place, not_in_word

def solve_wordle(
	word_set: List[str],
	wordle: Type[Wordle],
	settings: Dict[str, bool]=DEFAULT_SETTINGS,
	debug: bool=False
) -> Tuple[bool, int, List[str]]:
    clues = []
    for i in range(MAX_GUESSES):
        chosen, cands, numcands = guess_next_word(word_set, clues, settings=settings, debug=debug)
        if debug:
            print(f'Choosing [{chosen}]. Total {numcands} candidates: {cands}...')
        clue, state = wordle.guess(chosen)
        if clue:
            clues.append((chosen, clue))
        if state == Wordle.SOLVED:
            if debug:
                print(f'Woohoo! Solver solved it in {i+1} guesses!')
            return True, i+1, cands
        elif state == Wordle.UNSOLVED:
            if debug:
                print('Oh no, it beat the solver :(')
            return False, -1, cands

# Returns a tuple of 
# - a chosen next guess
# - a list of possible candidate words left to solve the wordle
# - the number of possible candidate words left
NON_POS_WEIGHT = 0.5
def guess_next_word(
	word_set: List[str],
	clues: List[Tuple[str, List[int]]],
	settings: Dict[str, bool]=DEFAULT_SETTINGS,
	debug=False
) -> Tuple[str, List[str], int]:
	N = get_n_from_word_set(word_set)
	word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues, debug=debug)
	prev_guesses = set([w for w, _ in clues])
	if len(clues) and clues[-1][1] == [GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT]:
		return None, [], 0

	cands = [w for w in word_set \
			if not w in prev_guesses and is_guessable_word(w, word_right_place, in_word_wrong_place, not_in_word)]
			
	char_freq_heuristic = defaultdict(int)
	if not settings['non_strict']:
		# TODO(deedy): Support use_pos when non_strict
		char_distribution_words = word_set
		if settings['use_conditional']:
			# Heuristic should be conditional on what is left!
			char_distribution_words = cands
		char_dist = Counter([l for c in char_distribution_words for l in c]).most_common()
		char_dist_freq = {let: freq for let, freq in char_dist}
		def sortfn(word):
			# Distinct letters num times appear
			return -sum([char_dist_freq[c] for c in set(word)])
		sortcands = sorted(cands, key=sortfn)
		chosen = sortcands[0]
		return chosen, sortcands, len(sortcands)
	
	
	
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
		# Does this happen? 
		import pdb; pdb.set_trace()
	if not settings['use_pos']:
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
			score = [0]*26
			nonpos_score = [0]*26
			for i, c in enumerate(word):
				# += does well also but performs worse for duplicate letters
				score[ord(c)-ord('a')] = conditional_pos_freq[i][c]
				nonpos_score[ord(c)-ord('a')] = conditional_unknown_freq[c] - conditional_pos_freq[i][c]
			sortscore = -(sum(score) + NON_POS_WEIGHT * sum(nonpos_score))
			if sort:
				return sortscore
			return ([(chr(i + ord('a')), v) for i, v in enumerate(score) if v],
					[(chr(i+ ord('a')), v) for i, v in enumerate(nonpos_score) if v], sortscore)
		sortfn = sort_maximal_position_with_nonpos
	
	explore_cands = sorted(word_set, key=sortfn)
	max_val = sortfn(explore_cands[0])
	explore_cands = [x for x in explore_cands if sortfn(x) == max_val]
	
	if len(explore_cands) > 0:
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
		explore_cands = sorted(explore_cands, key=boost_letters_in_right_place)
		max_val2 = boost_letters_in_right_place(explore_cands[0])
		explore_cands = [x for x in explore_cands if boost_letters_in_right_place(x) == max_val2]
	
	if debug: 
		print('Inferred conditions ', [''.join(m) for m in new_musts])
		cond_probs = [(x, y) for x, y in conditional_unknown_freq.items() if y]
		print(f'Conditional ({len(cond_probs)}):{cond_probs}\nCands ({len(cands)}): {cands[:100]}...\n')
		print(f'Explore cands ({len(explore_cands)}): {[(c, sortfn(c), boost_letters_in_right_place(c)) for c in explore_cands[:10]]}')

	chosen_cs = [cand for cand in explore_cands if cand not in prev_guesses]
	chosen = chosen_cs[0]	
	return chosen, cands[:5], len(cands)
	 