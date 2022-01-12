from collections import Counter
from dictionary import dictionary
from game.wordle import Wordle
from game.constants import N, MAX_GUESSES
from game.solver.solver import guess_next_word, solve_wordle
import argparse
import random
import sys
from time import time


PLAY = 'play'
SOLVE = 'solve'
SHOW = 'show'
EVAL = 'eval'

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
    args = parser.parse_args()
    five_words = dictionary.read_words_of_length(N)
    if args.mode == PLAY:
        hidden_word = random.choice(five_words)
        w = Wordle(five_words, hidden_word)
        while w.state == Wordle.PLAYING:
            # TODO(deedy): Add support for guessed letters in Wordle
            guess = input('Guess? ')
            try:
                clue, _ = w.guess(guess)
            except Exception as e:
                print(f'Error: {str(e)}')
    elif args.mode == SHOW:
        if not args.word and not args.random:
            print(f'Error: Must provide word to solve with -w/--word or -r/--random.')
            sys.exit() 
        try:
            word = args.word if args.word else random.choice(five_words)
            print(f'Word [{word.upper()}]')
            w = Wordle(five_words, word)
            solve_wordle(five_words, w, debug=args.debug)
        except Exception as e:
            print(f'Error: {str(e)}')
    elif args.mode == SOLVE:
        clues = []
        guesses = 0
        while guesses < MAX_GUESSES:
            chosen, cands, lencands = guess_next_word(five_words, clues, debug=args.debug)
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
    elif args.mode == EVAL:
        if args.word:
            words = args.word.split(',')
        else:
            K = args.k
            if not args.k:
                K = len(five_words)
            print(f'Evaluating on {K} words')
            words = random.sample(five_words, K)
        fails = []
        start = time()
        attempt_tot = 0
        for x in range(len(words)):
            count = x+1
            if count and count % 10 == 0:
                print(f'k={count}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/count)*100:.02f}%\tAvg Attempts: {attempt_tot/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')
            word = words[x]
            w = Wordle(five_words, word, verbose=False)
            got_ans, attempts, cands = solve_wordle(five_words, w, debug=False)
            attempt_tot += attempts
            if not got_ans:
                fails.append((word, len(cands)))
        failed_words = [f[0] for f in fails]
        print(f'Failed on: {failed_words}')
        print(f'Distribution of remaining candidates: {Counter([f[1] for f in fails]).most_common()}')
        print(f'K={len(words)}:\tFailed: {len(fails)}\tAccuracy:{(1 - len(fails)/len(words))*100:.02f}%\tAvg Attempts: {attempt_tot/count:.02f}\tAvg Time: {(time() - start)/count:.03f}s')


if __name__ == '__main__':
    main()
    # run tests: python -m unittest



