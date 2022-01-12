# Wordle Solver

The most comprehensive, exhaustive, parameterized command-line *wordle* (https://www.powerlanguage.co.uk/wordle/) solver. Wordle is a really popular game made viral by it's inscrutable and quirky emoticon-based game description.

The solver boasts a *99.35%+* accuracy on the 8636 valid 5-letter words. Features:
 - Supports 4 modes: `play`, `show` (to show a solution for a specific word), `solve` (to solve a puzzle online) and `eval` (evaluate the performance)
 - Deterministic
 - Highest accuracy of all solutions evaluated
 - Support custom dictionaries with `--dict_file`
 - Support custom length wordles with `-N` and custom max guesses with `--guesses`.
 - Supports "hard mode" where each guess must conform to previous hints with `--hard`.
 - Fully tested
 - Latency `~0.26s` per run on default ~9000 word dict and all 5 letter words.
Current dictionary used is the valid [Scrabble dictionary](https://github.com/zeisler/scrabble). 

Solver’s attempt to solve the Jan 10, 2022 wordle for the word `query`:

```
⬛🟨⬛⬛🟨 AROSE
⬛🟩⬛⬛⬛ TUMID
⬛⬛🟨⬛⬛ GLYPH
🟩🟩🟩🟩🟩 QUERY
```
<img width="196" alt="Screen Shot 2022-01-12 at 12 26 16 AM" src="https://user-images.githubusercontent.com/1846373/149004246-6f200c36-de13-4bb3-90a6-eb34d27047ce.png">


# Algorithm

With the settings for non-strict play, using positional
 - Find all candidates that fit the criteria
 - Amongst the valid candidates, compute a distribution of letters at each position
 - Find a word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i)
 - Repeat 

The 56 failure cases are `sakes`, `mooed`, `jived`, `wanes`, `jocks`, `minks`, `wades`, `jaded`, `zoner`, `joker`, `wived`, `jakes`, `mozos`, `goxes`, `vills`, `rover`, `zooks`, `cozes`, `jibes`, `wakes`, `hajes`, `joked`, `sinhs`, `zaxes`, `yaffs`, `hiker`, `bases`, `moved`, `bises`, `zills`, `hided`, `eaved`, `vined`, `surfs`, `jiber`, `gibed`, `dozer`, `fuzed`, `mixed`, `boxed`, `waxes`, `waves`, `vomer`, `egged`, `mazed`, `pests`, `hived`, `socks`, `fazes`, `vests`, `jibed`, `mewed`, `hazes`, `sooks`, `woods`, `sinks`
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

# Advanced Usage

### Custom settings

Here are things you can customize with each run:

 - `-d` Specify a debug level. `2` gives the most details, and `1`, the default if this flag is specified gives certain details like the length of the candidate set and what the previous clues tell us. 
 - `-N` Specify the length of the words in the wordle you want to play. Default is `5`. 
 - `--guesses` Specify the number of valid guesses. Default is `6`.
 - `-hard` Whether or not to play on "hard mode" where each subsequent guess must adhere to the previous clues. 
 - `--dict_file` The word set you want to use. Details below. 

### Specifying a dict file 

Results of the evaluation and performance of the eval depend greatly on the choice of dict file used. Here are some options provided by default. You can specify it (or add your own) with `--dict_file`

 - `data/dictionary_proper.txt`: 8636 5-letter words. A valid Scrabble dictionary, and the default choice. Source: https://github.com/zeisler/scrabble
 - `data/words_alpha.txt`: 15918 5-letter words. Contains strange words like `chivw`. Source: https://github.com/dwyl/english-words
 - `data/unix_words.txt`: 8497 lowercase 5-letter words. Source: Default `/usr/share/dict/words` on Mac machines.
 - `'data/lexicon_4958.txt`: 4958 5-letter words. Source: @dsivakumar's https://github.com/aravinho/wordle_public/blob/main/wordle/lexicons/lexicon_4958. Explanation on how this is derived is in the repo.
 - `data/sgb-words.txt`: 5757 5-letter words. The list of 5-letter words from Knuth's Stanford Graph Base. Source: https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt

The official Wordle game uses a large lexicon for valid guess words, but a smaller subset for valid magic words. We ignore this assumption and assume any valid word can be guessed. 

# Evaluation 

Using a dictionary of scrabble words, there are 172,819 total words and around 5% of them are exactly 5 letters long (8,636). The algorithm devised achieves a *99.28%* success rate at guessing the right word, failing to get the correct the answer for 62 words.

Other settings achieved:
 - Global character frequency heuristic: Couldn't solve for 133 out of 1000 random samples (86.7% Success rate)
 - Conditional character frequency heuristic, on candidates left: Couldn't solve for 100 out of 1000 random samples (90.0% Success rate)
 - Non-strict solution: Couldn't solve for 46 out of 1000 random samples (95.4% Success rate)
 - Position-aware frequency heuristic + bug fixes: Couldn't solve for 9 out of 1000 random samples (99.1% Success rate)

Using other values of `N` with `MAX_GUESSES=6`, with the optimal solver:
 - N=2 (96 words) `K=96:	Failed: 32	Accuracy:66.67%	Avg Attempts: 2.67	Avg Time: 0.002s`
 - N=3 (972 words) `K=100:	Failed: 23	Accuracy:77.00%	Avg Attempts: 3.69	Avg Time: 0.030s`
 - N=4 (3903 words) `K=100:	Failed: 5	Accuracy:95.00%	Avg Attempts: 4.46	Avg Time: 0.116s`
 - N=5 (8636 words) `K=100:	Failed: 1	Accuracy:99.00%	Avg Attempts: 4.13	Avg Time: 0.241s`
 - N=6 (15232 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 3.83	Avg Time: 0.471s`
 - N=7 (23109 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 3.58	Avg Time: 0.678s`
 - N=8 (28420 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 3.25	Avg Time: 0.819s`
 - N=9 (24873 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 3.00	Avg Time: 0.728s`
 - N=10 (20300 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 2.86	Avg Time: 0.643s`
 - N=11 (15504 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 2.64	Avg Time: 0.468s`
 - N=12 (11357 words) `K=100:	Failed: 0	Accuracy:100.00%	Avg Attempts: 2.45	Avg Time: 0.327s`

# Future Work

 - Support passing in solver settings through command line, including the weight of `NON_POS_WEIGHT`
 - Support passing in a custom dictionary through settings
 - Expose customizable number of letters in the word (`N`) and `MAX_GUESSES`.
