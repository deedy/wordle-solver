from typing import Dict, List, Tuple
from .constants import NOTHING, GUESS_WRONG_SPOT, GUESS_RIGHT_SPOT, DEFAULT_GAME_CONFIG
from .util import get_n_from_word_set

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
    
    def __init__(self, word_set: List[str], word: str, config: Dict[str, str] = DEFAULT_GAME_CONFIG,verbose=True):
        self.N = get_n_from_word_set(word_set)
        self.MAX_GUESSES = int(config['max_guesses'])
        self.all_words = set(word_set)
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
        if len(guess) != self.N:
            raise Exception(f'[{guess}] needs to be {self.N} letters')
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
        clue = [NOTHING] * self.N
        for i, g in enumerate(guess):
            if self._word[i] == g:
                clue[i] = GUESS_RIGHT_SPOT
            elif g in self._word:
                clue[i] = GUESS_WRONG_SPOT
        if self.verbose:
            print(guess.upper())
            print(Wordle.emojify(clue))
            
        if len([1 for c in clue if c == GUESS_RIGHT_SPOT]) == self.N:
            if self.verbose:
                print(f'Solved! - [{guess}]')
            self.state = Wordle.SOLVED
        elif len(self.guesses) >= self.MAX_GUESSES:
            if self.verbose:
                print(f'Lost! Word was [{self._word}] - {self.guesses}')
            self.state = Wordle.UNSOLVED
        
        return clue, self.state