# TODO(deedy): Make enums
DEFAULT_N = 5
DEFAULT_MAX_GUESSES = 6
DATA_DIR = 'data'
DEFAULT_DICT = 'data/official_wordle_all.txt'
DEFAULT_CAND_DICT = 'data/official_wordle_common.txt'

# Game settings
DEFAULT_GAME_CONFIG = {
    'max_guesses': str(DEFAULT_MAX_GUESSES),
	# The set of words that can potentially be solutions
	'candidate_set': [],
	# The set of words that can be guessed validly
	'guess_set': []
}

# Solver settings
DEFAULT_SOLVER_SETTINGS = {
	# This now on by default. The setting was retired becuse it's inefficient and adding tech debt.
	# Not needed to implement unless we want to test for this specifically
	# 'use_conditional': True,
	# "HARD mode" - every subsequent guess must be in the candidate set
	'non_strict': True,
	# Use positional character distribution instead of global character distribution amongst the 
	# remaining word candidates.
	'use_pos': True,
	'max_guesses': str(DEFAULT_MAX_GUESSES),
	'non_pos_weight': str(0.5),
	# The set of words that can potentially be solutions
	'candidate_set': [],
	# The set of words that can be guessed validly
	'guess_set': [],
	# If present, a tree that solves the entire wordle. If the wrong tree is provided for the wrong dict settings, it will be 
	# erroneous
	'solution_tree': {}
}

# tile
NOTHING = 0
GUESS_WRONG_SPOT = 1
GUESS_RIGHT_SPOT = 2

