from collections import Counter
from game.wordle import Wordle
from game.constants import DEFAULT_N, DEFAULT_MAX_GUESSES, DEFAULT_GAME_CONFIG, DEFAULT_SOLVER_SETTINGS, DEFAULT_DICT, DEFAULT_CAND_DICT
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


def play(game_config: Dict[str, str]):
    hidden_word = random.choice(game_config['candidate_set'])
    w = Wordle(hidden_word, config=game_config)
    while w.state == Wordle.PLAYING:
        # TODO(deedy): Add support for guessed letters in Wordle
        guess = input('Guess? ')
        try:
            clue, _ = w.guess(guess)
        except Exception as e:
            print(f'Error: {str(e)}')

def show(words: List[str], game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    for word in words:
        try:
            print(f'Word [{word.upper()}]')
            w = Wordle(word, config=game_config)
            solve_wordle(w, solver_settings=solver_settings, debug=debug)
        except Exception as e:
            print(f'Error: {str(e)}')
        print('\n\n')

def solve(game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    if not 'guess_set' in solver_settings: 
        raise Exception('guess_set not specified in config')
    N = get_n_from_word_set(solver_settings['guess_set'])
    clues = []
    guesses = 0
    while guesses < int(game_config['max_guesses']):
        chosen, cands, lencands = guess_next_word(clues, solver_settings=solver_settings, debug=debug)
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

def eval(words: List[str], out_file: str, game_config: Dict[str, str], solver_settings: Dict[str, str], debug: int=0):
    if not 'candidate_set' in solver_settings: 
        raise Exception('candidate_set not specified in config')
    candidates = solver_settings['candidate_set']
    print(f'Evaluating on {len(words)} words. Total available candidate words: {len(candidates)}')
    fails = []
    start = time()
    attempts = []
    attempt_tot = 0
    for x in range(len(words)):
        count = x+1
        if count and count % 10 == 0:
            print(f'k={count}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/count)*100:.02f}%\tAvg Attempts: {sum([len(a[1]) for a in attempts])/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')
        word = words[x]
        w = Wordle(word, config=game_config, verbose=debug >= 2)
        solv = time()
        got_ans, attempt_count, cands = solve_wordle(w, solver_settings=solver_settings, debug=debug)
        print(f'Run {time()-solv:0.3f}s')
        if not got_ans:
            fails.append((word, w.guesses))
        else:
            attempts.append((word, w.guesses))
    failed_words = [f[0] for f in fails]
    print(f'Failed on: {failed_words}')
    print(f'Distribution of remaining candidates: {Counter([len(f[1]) for f in fails]).most_common()}')
    print(f'Distribution of attempts needed: {Counter([len(a[1]) for a in attempts]).most_common()}')
    print(f'K={len(words)}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/len(words))*100:.02f}%\tAvg Attempts: {sum([len(a[1]) for a in attempts])/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')
    if out_file:
        print(f'Writing raw results to file [{out_file}]')
        # Potentially create custom out_file name if not provided
        headers = ['word', 'solved', 'guesses', 'attempts']
        with open(out_file, 'w') as f:
            f.write(','.join(headers)+'\n')
            for fail in fails:
                f.write(','.join([fail[0], '0', '-'.join(fail[1]), str(len(fail[1]))]) + '\n')
            for attempt in attempts:
                f.write(','.join([attempt[0], '1', '-'.join(attempt[1]), str(len(attempt[1]))]) + '\n')

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
    parser.add_argument('--cand_file',
                        type=str,
                        help='Dictionary file to read potential candidate set from. If not provided, dict_file is used.',
                        default=DEFAULT_CAND_DICT,
                        required=False)
    parser.add_argument('--eval_out_file',
                        type=str,
                        help='A file to write the detailed outputs for the eval to.',
                        default=None,
                        required=False)
    args = parser.parse_args()
    N = args.N
    if args.dict_file != DEFAULT_DICT:
        print(f'Using the same candidates as dict_file: [{args.dict_file}]')
        args.cand_file = args.dict_file
    try:
        word_set = read_words_of_length(N, fname=args.dict_file)
        if args.debug >= 1:
            print(f'Read {len(word_set)} valid lower case words from [{args.dict_file}]')
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit()
    if args.cand_file:
        try:
            candidate_set = read_words_of_length(N, fname=args.cand_file)
            if args.debug >= 1:
                print(f'Read {len(candidate_set)} valid lower case candidate words from [{args.cand_file}]')
        except Exception as e:
            print(f'Error: {str(e)}')
            sys.exit()
    else:
        if args.debug >= 1:
            print(f'Using the same candidate_set as word_set')
        candidate_set = word_set
    game_config = DEFAULT_GAME_CONFIG
    game_config['max_guesses'] = str(args.guesses)
    game_config['candidate_set'] = candidate_set
    game_config['guess_set'] = word_set
    solver_settings = DEFAULT_SOLVER_SETTINGS
    solver_settings['max_guesses'] = str(args.guesses)
    solver_settings['non_strict'] = not args.hard_mode
    solver_settings['candidate_set'] = candidate_set
    solver_settings['guess_set'] = word_set
    if args.mode == PLAY:
        play(game_config=game_config)
    elif args.mode == SHOW:
        if not args.word and not args.random:
            print(f'Error: Must provide word to solve with -w/--word or -r/--random.')
            sys.exit() 
        words = args.word.split(',') if args.word else [random.choice(solver_settings['candidate_set'])]
        show(words, game_config=game_config, solver_settings=solver_settings, debug=args.debug)
    elif args.mode == SOLVE:
        solve(game_config=game_config, solver_settings=solver_settings, debug=args.debug)
    elif args.mode == EVAL:
        if not args.eval_out_file:
            print(f'Running eval. Specify --eval_out_file to write the details of the eval to a file.')
        if args.word:
            words = args.word.split(',')
        else:
            K = args.k
            if not args.k:
                K = len(solver_settings['candidate_set'])
            words = random.sample(solver_settings['candidate_set'], K)
        eval(words, args.eval_out_file, game_config=game_config, solver_settings=solver_settings)    


if __name__ == '__main__':
    main()
    # run tests: python -m unittest



