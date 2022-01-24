from typing import Dict, List, Tuple, Set
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
    
    def __init__(self, word: str, config: Dict[str, str] = DEFAULT_GAME_CONFIG, verbose=True):
        self._word = word.lower()
        if not 'candidate_set' in config or not len(config['candidate_set']): 
            raise Exception('candidate_set not specified in config')
        self.candidate_set = set(config['candidate_set'])
        self.N = get_n_from_word_set(config['candidate_set'])
        self.MAX_GUESSES = int(config['max_guesses'])
        Wordle.check_word(self.N, self._word, self.candidate_set)

        if not 'guess_set' in config or not len(config['guess_set']): 
            self.guess_set = set(config['candidate_set'])
        else:
            self.guess_set = set(config['guess_set'])

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

    def check_word(N: int, guess: str, word_set: Set[str]):
        if len(guess) != N:
            raise Exception(f'[{guess}] needs to be {self.N} letters')
        if not guess in word_set:
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
        Wordle.check_word(self.N, guess, self.guess_set)
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