# TODO(deedy): Make enums
DEFAULT_N = 5
DEFAULT_MAX_GUESSES = 6
DATA_DIR = 'data'
DEFAULT_DICT = 'data/dictionary_proper.txt'

# Game settings
DEFAULT_GAME_CONFIG = {
    'max_guesses': str(DEFAULT_MAX_GUESSES)
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
	'max_guesses': str(DEFAULT_MAX_GUESSES)
}

# tile
NOTHING = 0
GUESS_WRONG_SPOT = 1
GUESS_RIGHT_SPOT = 2

