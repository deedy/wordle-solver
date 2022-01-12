# TODO(deedy): Make enums
DEFAULT_N = 5
DEFAULT_MAX_GUESSES = 6

# Game settings
DEFAULT_GAME_CONFIG = {
    'max_guesses': str(DEFAULT_MAX_GUESSES)
}

# Solver settings
DEFAULT_SOLVER_SETTINGS = {
	'use_conditional': True,
	'non_strict': True,
	'use_pos': True,
	'max_guesses': str(DEFAULT_MAX_GUESSES)
}

# tile
NOTHING = 0
GUESS_WRONG_SPOT = 1
GUESS_RIGHT_SPOT = 2

