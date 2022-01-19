from collections import Counter
from game.wordle import Wordle
from game.constants import DEFAULT_N, DEFAULT_MAX_GUESSES, DEFAULT_GAME_CONFIG, DEFAULT_SOLVER_SETTINGS, DEFAULT_DICT
from game.solver.solver import guess_next_word, solve_wordle
from game.util import get_n_from_word_set, read_words_of_length
import argparse
import random
import sys
from time import time
from typing import Dict, List


PLAY = 'play'
SOLVE = 'solve'
SHOW = 'show'
EVAL = 'eval'


def play(word_set: List[str], game_config: Dict[str, str]):
    hidden_word = random.choice(word_set)
    w = Wordle(word_set, hidden_word, config=game_config)
    while w.state == Wordle.PLAYING:
        # TODO(deedy): Add support for guessed letters in Wordle
        guess = input('Guess? ')
        try:
            clue, _ = w.guess(guess)
        except Exception as e:
            print(f'Error: {str(e)}')

def show(word_set: List[str], words: List[str], game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    for word in words:
        try:
            print(f'Word [{word.upper()}]')
            w = Wordle(word_set, word, config=game_config)
            solve_wordle(word_set, w, solver_settings=solver_settings, debug=debug)
        except Exception as e:
            print(f'Error: {str(e)}')
        print('\n\n')

def solve(word_set: List[str], game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    N = get_n_from_word_set(word_set)
    clues = []
    guesses = 0
    while guesses < int(game_config['max_guesses']):
        chosen, cands, lencands = guess_next_word(word_set, clues, solver_settings=solver_settings, debug=debug)
        if not chosen:
            print(f'Solved! = {clues[-1][0]}')
            sys.exit()
        print(f'Try the word [{chosen.upper()}]. There are {lencands} possible words: {cands[:10]}...')
        feedback = input('How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? ')
        if len(feedback) != N:
            print(f'Error: Result must be {N} length.')
            continue
        if len(set(feedback + '012')) > 3:
            print(f'Error: Must only be 0, 1, or 2')
            continue
        guesses += 1
        feedback_parsed = [ord(f) - ord('0') for f in feedback]
        clues.append((chosen, feedback_parsed)) 
    print(f'Unsolved!')

def eval(word_set: List[str], words: List[str], game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    print(f'Evaluating on {len(words)} words. Total available words: {len(word_set)}')
    fails = []
    start = time()
    attempts = []
    attempt_tot = 0
    for x in range(len(words)):
        count = x+1
        if count and count % 10 == 0:
            print(f'k={count}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/count)*100:.02f}%\tAvg Attempts: {sum([a[1] for a in attempts])/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')
        word = words[x]
        w = Wordle(word_set, word, config=game_config, verbose=debug >= 2)
        got_ans, attempt_count, cands = solve_wordle(word_set, w, solver_settings=solver_settings, debug=debug)
        if not got_ans:
            fails.append((word, len(cands)))
        else:
            attempts.append((word, attempt_count))
    failed_words = [f[0] for f in fails]
    print(f'Failed on: {failed_words}')
    print(f'Distribution of remaining candidates: {Counter([f[1] for f in fails]).most_common()}')
    print(f'Distribution of attempts needed: {Counter([a[1] for a in attempts]).most_common()}')
    print(f'K={len(words)}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/len(words))*100:.02f}%\tAvg Attempts: {attempt_tot/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')

def main():
    parser = argparse.ArgumentParser(description='Play Wordle')
    parser.add_argument('-m',
                        '--mode',
                        help='Run mode. Default none',
                        choices=[PLAY, SHOW, SOLVE, EVAL],
                        default=None,
                        required=True)
    parser.add_argument('-w',
                        '--word',
                        help='Word to solve for in solve mode, or list of comma-separated words for eval',
                        default=None,
                        required=False)
    parser.add_argument('-r',
                        '--random',
                        action='store_true',
                        help='Random word to solve for',
                        default=True,
                        required=False)
    parser.add_argument('-k',
                        type=int,
                        help='Number of candidates to eval when -m eval',
                        default=None,
                        required=False)
    parser.add_argument('-d',
                        '--debug',
                        type=int,
                        help='Debug mode or not',
                        default=0,
                        nargs='?',
                        const=1,
                        required=False)
    parser.add_argument('-N',
                        type=int,
                        help='Value of N - the length of the word',
                        default=DEFAULT_N,
                        required=False)
    parser.add_argument('--guesses',
                        type=int,
                        help='Value of MAX_GUESSES',
                        default=DEFAULT_MAX_GUESSES,
                        required=False)
    parser.add_argument('-hard',
                        '--hard_mode',
                        action='store_true',
                        help='Wordle in "hard mode" or not which requires all guesses to conform to the previous clues.',
                        default=False,
                        required=False)
    parser.add_argument('--dict_file',
                        type=str,
                        help='Dictionary file to read from',
                        default=DEFAULT_DICT,
                        required=False)
    args = parser.parse_args()
    N = args.N
    try:
        word_set = read_words_of_length(N, fname=args.dict_file)
        if args.debug >= 1:
            print(f'Read {len(word_set)} valid lower case words from [{args.dict_file}]')
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit()
    game_config = DEFAULT_GAME_CONFIG
    game_config['max_guesses'] = str(args.guesses)
    solver_settings = DEFAULT_SOLVER_SETTINGS
    solver_settings['max_guesses'] = str(args.guesses)
    solver_settings['non_strict'] = not args.hard_mode
    if args.mode == PLAY:
        play(word_set, game_config=game_config)
    elif args.mode == SHOW:
        if not args.word and not args.random:
            print(f'Error: Must provide word to solve with -w/--word or -r/--random.')
            sys.exit() 
        words = args.word.split(',') if args.word else [random.choice(word_set)]
        show(word_set, words, game_config=game_config, solver_settings=solver_settings, debug=args.debug)
    elif args.mode == SOLVE:
        solve(word_set, game_config=game_config, solver_settings=solver_settings, debug=args.debug)
    elif args.mode == EVAL:
        if args.word:
            words = args.word.split(',')
        else:
            K = args.k
            if not args.k:
                K = len(word_set)
            words = random.sample(word_set, K)
        eval(word_set, words, game_config=game_config, solver_settings=solver_settings)    


if __name__ == '__main__':
    main()
    # run tests: python -m unittest



