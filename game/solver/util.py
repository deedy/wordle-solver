from typing import List, Dict, Set

def indexall(w: str, let: str) -> Set[int]:
    ix = set()
    for i in range(len(w)):
        if w[i] == let:
            ix.add(i)
    return ix

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