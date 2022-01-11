from typing import List, Tuple
from .constants import N, MAX_GUESSES, NOTHING, GUESS_WRONG_SPOT, GUESS_RIGHT_SPOT

class Wordle:
    EMOJI_MAP = {
        NOTHING: '⬛',
        GUESS_WRONG_SPOT: '🟨',
        GUESS_RIGHT_SPOT: '🟩',
    }
    # states
    PLAYING = 0
    SOLVED = 1
    UNSOLVED = 2
    
    def __init__(self, five_words: List[str], word: str, verbose=True):
        self.all_words = five_words
        self.check_word(word)
        self._word = word.lower()
        self.guesses = []
        self.state = Wordle.PLAYING
        self.verbose = verbose
    
    def emojify(clue):
        pclue = []
        for c in clue:
            if not c in Wordle.EMOJI_MAP:
                assert False 
            pclue.append(Wordle.EMOJI_MAP[c]) 
        return ''.join(pclue)

    def check_word(self, guess):
        if len(guess) != N:
            raise Exception(f'[{guess}] needs to be {N} letters')
        if not guess in self.all_words:
            raise Exception(f'[{guess}] is not a valid word!')

    
    # Encoding: 0, nothing, 1 guess wrong spot, 2 guess right spot
    def guess(self, guess: str) -> Tuple[List[str], int]:
        if self.state == Wordle.SOLVED:
            if self.verbose:
                print('Already solved!')
            return None, self.state
        if self.state == Wordle.UNSOLVED:
            if self.verbose:
                print('Already lost!')
            return None, self.state
        guess = guess.lower()
        self.check_word(guess)
        self.guesses.append(guess)
        clue = [NOTHING] * N
        for i, g in enumerate(guess):
            if self._word[i] == g:
                clue[i] = GUESS_RIGHT_SPOT
            elif g in self._word:
                clue[i] = GUESS_WRONG_SPOT
        if self.verbose:
            print(guess.upper())
            print(Wordle.emojify(clue))
            
        if len([1 for c in clue if c == GUESS_RIGHT_SPOT]) == N:
            if self.verbose:
                print(f'Solved! - {guess}')
            self.state = Wordle.SOLVED
        elif len(self.guesses) >= MAX_GUESSES:
            if self.verbose:
                print(f'Lost! - {self.guesses}')
            self.state = Wordle.UNSOLVED
        
        return clue, self.state