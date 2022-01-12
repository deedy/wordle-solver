from typing import List, Dict, Set, Tuple
from collections import defaultdict
from ..constants import NOTHING, GUESS_WRONG_SPOT, GUESS_RIGHT_SPOT

def indexall(w: str, let: str) -> Set[int]:
    ix = set()
    for i in range(len(w)):
        if w[i] == let:
            ix.add(i)
    return ix

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

def is_guessable_word(
        w: str,
        word_right_place: Dict[str, Set[int]],
        in_word_wrong_place: Dict[str, Set[int]],
        not_in_word: Set[str],
        debug: bool=False
    ) -> bool:
    for let in word_right_place.keys():
        if not let in w:
            if debug:
                print(f'Letter [{let}] needs to be in word (in right order)!')
            return False
        for ix in word_right_place[let]:
            if not ix in indexall(w, let):
                if debug:
                    print(f'Letter [{let}] needs to be in word at [{word_right_place[let]}] - {ix} {w}, {indexall(w, let)}')
                return False
    for let in in_word_wrong_place.keys():
        if not let in w:
            if debug:
                print(f'Letter [{let}] needs to be in word!')
            return False
        for ix in indexall(w, let):
            if ix in in_word_wrong_place[let]:
                if debug:
                    print(f'Letter [{let}] needs to be in word and NOT at [{in_word_wrong_place[let]}]')
                return False
    for let in not_in_word:
        if let in w:
            if debug:
                print(f'Letter [{let}] cannot be in word!')
            return False
    return True