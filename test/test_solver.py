import unittest
from game.solver.solver import guess_next_word, parse_clues
from game.constants import DEFAULT_SOLVER_SETTINGS

class TestUtils(unittest.TestCase):

	def test_parse_clues(self):
		word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues = [('binks', [0, 2, 2, 2, 2])])
		self.assertEqual(not_in_word, set('b'), "Guess not_in_word")
		self.assertEqual(in_word_wrong_place, {}, "Guess in_word_wrong_place")
		self.assertEqual(word_right_place, {'i': set([1]), 'n': set([2]), 'k': set([3]), 's': set([4])}, "Guess word_right_place")

		word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues = [('binks', [0, 1, 1, 1, 1])])
		self.assertEqual(not_in_word, set('b'), "Guess not_in_word")
		self.assertEqual(in_word_wrong_place, {'i': set([1]), 'n': set([2]), 'k': set([3]), 's': set([4])}, "Guess in_word_wrong_place")
		self.assertEqual(word_right_place, {}, "Guess word_right_place")

		word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues = [('binks', [0, 0, 0, 0, 0])])
		self.assertEqual(not_in_word, set('binks'), "Guess not_in_word")
		self.assertEqual(in_word_wrong_place, {}, "Guess in_word_wrong_place")
		self.assertEqual(word_right_place, {}, "Guess word_right_place")

	def test_guess_next_word_no_options(self):
		# Tests that a "no candidate" exception is raised if there's no suitable candidates
		clues = [('arose', [0, 0, 0, 0, 0])]
		settings = DEFAULT_SOLVER_SETTINGS

		# Raise exception if no possible candidates
		settings['candidate_set'] = []
		with self.assertRaises(Exception) as context:
			guess, cands, lencands = guess_next_word(clues, solver_settings=settings)

		# Raise if possible candidates have already been used
		settings['candidate_set'] = ['arose']
		with self.assertRaises(Exception) as context:
			guess, cands, lencands = guess_next_word(clues, solver_settings=settings)

	def test_guess_next_word_avoid_duplicates(self):
		clues = [('arose', [0, 0, 0, 0, 0])]
		settings = DEFAULT_SOLVER_SETTINGS
		settings['candidate_set'] = ['arose', 'unlit']
		guess, cands, lencands = guess_next_word(clues, solver_settings=settings)
		self.assertEqual(guess, 'unlit', "Guess correctly")
		self.assertEqual(cands, ['unlit'], "Candidates correctly")
		self.assertEqual(lencands, 1, "Num candidates correctly")

	def test_guess_next_word(self):
		clues = [('binks', [0, 2, 2, 2, 2])]
		settings = DEFAULT_SOLVER_SETTINGS
		settings['candidate_set'] = ['binks', 'cinks', 'dinks', 'einks', 'finks', 'ginks', 'hinks', 'abcde']
		guess, cands, lencands = guess_next_word(clues, solver_settings=settings)
		self.assertEqual(guess, 'abcde', "Guess correctly")
		self.assertEqual(lencands, len(settings['candidate_set']) - 2, "Num candidates correctly")
		clues = [('binks', [0, 2, 2, 2, 2]), ('abcde', [0, 0, 0, 0, 0])]
		guess, cands, lencands = guess_next_word(clues, solver_settings=settings)
		# guesses next word in list without exploring
		self.assertEqual(guess, 'finks', "Guess correctly")
		self.assertEqual(lencands, 3, "Num candidates correctly")


if __name__ == '__main__':
	unittest.main()