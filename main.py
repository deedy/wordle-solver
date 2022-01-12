from collections import Counter
from dictionary import dictionary
from game.wordle import Wordle
from game.constants import DEFAULT_N, MAX_GUESSES
from game.solver.solver import guess_next_word, solve_wordle
from game.util import get_n_from_word_set
import argparse
import random
import sys
from time import time
from typing import List


PLAY = 'play'
SOLVE = 'solve'
SHOW = 'show'
EVAL = 'eval'


def play(word_set: List[str]):
    hidden_word = random.choice(word_set)
    w = Wordle(word_set, hidden_word)
    while w.state == Wordle.PLAYING:
        # TODO(deedy): Add support for guessed letters in Wordle
        guess = input('Guess? ')
        try:
            clue, _ = w.guess(guess)
        except Exception as e:
            print(f'Error: {str(e)}')

def show(word_set: List[str], words: List[str], debug=False):
    for word in words:
        try:
            print(f'Word [{word.upper()}]')
            w = Wordle(word_set, word)
            solve_wordle(word_set, w, debug=debug)
        except Exception as e:
            print(f'Error: {str(e)}')
        print('\n\n')

def solve(word_set: List[str], debug=False):
    N = get_n_from_word_set(word_set)
    clues = []
    guesses = 0
    while guesses < MAX_GUESSES:
        chosen, cands, lencands = guess_next_word(word_set, clues, debug=debug)
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

def eval(word_set: List[str], words: List[str]):
    print(f'Evaluating on {len(words)} words. Total available words: {len(word_set)}')
    fails = []
    start = time()
    attempt_tot = 0
    for x in range(len(words)):
        count = x+1
        if count and count % 10 == 0:
            print(f'k={count}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/count)*100:.02f}%\tAvg Attempts: {attempt_tot/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')
        word = words[x]
        w = Wordle(word_set, word, verbose=False)
        got_ans, attempts, cands = solve_wordle(word_set, w, debug=False)
        attempt_tot += attempts
        if not got_ans:
            fails.append((word, len(cands)))
    failed_words = [f[0] for f in fails]
    print(f'Failed on: {failed_words}')
    print(f'Distribution of remaining candidates: {Counter([f[1] for f in fails]).most_common()}')
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
                        action='store_true',
                        help='Debug mode or not',
                        default=False,
                        required=False)
    parser.add_argument('-N',
                        type=int,
                        help='Value of N',
                        default=DEFAULT_N,
                        required=False)
    args = parser.parse_args()
    N = args.N
    word_set = dictionary.read_words_of_length(N)
    if args.mode == PLAY:
        play(word_set)
    elif args.mode == SHOW:
        if not args.word and not args.random:
            print(f'Error: Must provide word to solve with -w/--word or -r/--random.')
            sys.exit() 
        words = args.word.split(',') if args.word else [random.choice(word_set)]
        show(word_set, words, debug=args.debug)
    elif args.mode == SOLVE:
        solve(word_set, debug=args.debug)
    elif args.mode == EVAL:
        if args.word:
            words = args.word.split(',')
        else:
            K = args.k
            if not args.k:
                K = len(word_set)
            words = random.sample(word_set, K)
        eval(word_set, words)    


if __name__ == '__main__':
    main()
    # run tests: python -m unittest



