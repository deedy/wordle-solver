# Wordle Solver

The most comprehensive, exhaustive, parameterized command-line *wordle* (https://www.powerlanguage.co.uk/wordle/) solver. Wordle is a really popular game made viral by it's inscrutable and quirky emoticon-based game description.

The solver boasts a *99.28%+* accuracy on the 8636 valid 5-letter words. Features:
 - Supports 4 modes: `play`, `show` (to show a solution for a specific word), `solve` (to solve a puzzle online) and `eval` (evaluate the performance)
 - Deterministic
 - Highest accuracy of all solutions evaluated
 - Fully tested
 - Latency `~0.26s` per run
Current dictionary used is the valid [Scrabble dictionary](https://github.com/zeisler/scrabble). 

Solver’s attempt to solve the Jan 10, 2022 wordle for the word `query`:
⬛🟨⬛⬛🟨
⬛🟩⬛⬛⬛
⬛⬛🟨⬛⬛
🟩🟩🟩🟩🟩
<img width="196" alt="Screen Shot 2022-01-12 at 12 26 16 AM" src="https://user-images.githubusercontent.com/1846373/149004246-6f200c36-de13-4bb3-90a6-eb34d27047ce.png">


# Algorithm

With the settings for non-strict play, using positional
 - Find all candidates that fit the criteria
 - Amongst the valid candidates, compute a distribution of letters at each position
 - Find a word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i)
 - Repeat 

Failure cases include `jived`, `hides`, `razer`, `zooks`, `jills`, `gibed`, `wises`, `yipes`, `wipes`, `sises`.
For all these words, there are 2-5 candidate words left at the last guess, and with a random last guess, there is a probability of guessing these too.

# Usage

### Play it yourself

`python main.py -m play`

```
Guess? tares
TARES
⬛🟩🟨⬛⬛
Guess? unlit
UNLIT
⬛⬛⬛⬛⬛
Guess? raver
RAVER
🟨🟩🟩⬛🟩
Guess? favor
FAVOR
🟩🟩🟩🟩🟩
Solved! - favor
```

### Solve for an unknown word

`python main.py -m solve`

```
Try the word [TARES]. There are 8636 possible words: ['aahed', 'aalii', 'aargh', 'abaca', 'abaci']...
How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? 00000
Try the word [NOILY]. There are 575 possible words: ['biddy', 'biffy', 'bifid', 'bigly', 'bijou']...
How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? 02002
Try the word [DHOBI]. There are 39 possible words: ['bobby', 'boggy', 'booby', 'boogy', 'boomy']...
How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? 20100
Try the word [DODGY]. There are 3 possible words: ['dodgy', 'doggy', 'dowdy']...
How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? 22122
Try the word [DOGGY]. There are 1 possible words: ['doggy']...
How did it do (0=⬛, 1=🟨, 2=🟩) e.g. 00000? 22222
Solved! = doggy
```

### Show a solution for a specific word

`python main.py -m show -w oozed`

```
Word [OOZED]
Choosing [tares]. Total 8636 candidates: ['aahed', 'aalii', 'aargh', 'abaca', 'abaci']...
TARES
⬛⬛⬛🟩⬛
Choosing [coled]. Total 288 candidates: ['bedel', 'bedew', 'bevel', 'bezel', 'bided']...
COLED
⬛🟩⬛🟩🟩
Choosing [howdy]. Total 31 candidates: ['boded', 'boned', 'booed', 'bowed', 'boxed']...
HOWDY
⬛🟩⬛🟨⬛
Choosing [bipod]. Total 16 candidates: ['boded', 'boned', 'booed', 'boxed', 'domed']...
BIPOD
⬛⬛⬛🟨🟩
Choosing [dozen]. Total 8 candidates: ['domed', 'dozed', 'foxed', 'joked', 'mooed']...
DOZEN
🟨🟩🟩🟩⬛
Choosing [oozed]. Total 1 candidates: ['oozed']...
OOZED
🟩🟩🟩🟩🟩
Solved! - oozed
Woohoo! Solver solved it in 6 guesses!
```

### Evaluate its performance

`python main.py -m eval -k 1000`

```
Evaluating on 1000 words
k=10:	Failed: 1	Accuracy:90.00%	Avg Time: 0.258s
k=20:	Failed: 1	Accuracy:95.00%	Avg Time: 0.250s
k=30:	Failed: 1	Accuracy:96.67%	Avg Time: 0.249s
k=40:	Failed: 1	Accuracy:97.50%	Avg Time: 0.244s
k=50:	Failed: 1	Accuracy:98.00%	Avg Time: 0.239s
...
k=970:	Failed: 10	Accuracy:98.97%	Avg Time: 0.236s
k=980:	Failed: 10	Accuracy:98.98%	Avg Time: 0.236s
k=990:	Failed: 10	Accuracy:98.99%	Avg Time: 0.236s
Failed on: ['jived', 'hides', 'razer', 'zooks', 'jills', 'gibed', 'wises', 'yipes', 'wipes', 'sises']
Distribution of remaining candidates: [(4, 5), (3, 3), (2, 1), (5, 1)]
K=999:	Failed: 10	Accuracy:99.00%
```

### Run Tests

`python -m unittest` runs the entire test suite. 

# Evaluation 

Using a dictionary of scrabble words, there are 172,819 total words and around 5% of them are exactly 5 letters long (8,636). The algorithm devised achieves a *99.28%* success rate at guessing the right word, failing to get the correct the answer for 62 words.

Other settings achieved:
 - Global character frequency heuristic: Couldn't solve for 133 out of 1000 random samples (86.7% Success rate)
 - Conditional character frequency heuristic, on candidates left: Couldn't solve for 100 out of 1000 random samples (90.0% Success rate)
 - Non-strict solution: Couldn't solve for 46 out of 1000 random samples (95.4% Success rate)
 - Position-aware frequency heuristic + bug fixes: Couldn't solve for 9 out of 1000 random samples (99.1% Success rate)

# Future Work

 - Support passing in solver settings through command line, including the weight of `NON_POS_WEIGHT`
 - Support passing in a custom dictionary through settings
 - Expose customizable number of letters in the word (`N`) and `MAX_GUESSES`.
