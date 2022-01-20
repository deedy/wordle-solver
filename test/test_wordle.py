import unittest
from game.wordle import Wordle

GAME_CONFIG = {}

class TestWordle(unittest.TestCase):

	def test_invalid_word_list(self):
		with self.assertRaises(Exception) as context:
			w = Wordle('gorge', config={'candidate_set': ['gorge', 'gorges']})
		with self.assertRaises(Exception) as context:
			w = Wordle('gorge', config={'candidate_set': []})

	def test_solved(self):
		w = Wordle('gorge', config={'candidate_set': ['gorge'], 'max_guesses': '6'})
		clue, state = w.guess('gorge')
		self.assertEqual(state, Wordle.SOLVED, "Should be solved!")
		self.assertEqual(Wordle.emojify(clue), '🟩🟩🟩🟩🟩', "Should be solved!")

	def test_missed_all(self):
		w = Wordle('gorge', config={'candidate_set': ['gorge', 'unlit'], 'max_guesses': '6'})
		clue, state = w.guess('unlit')
		self.assertEqual(state, Wordle.PLAYING, "Should be playing!")
		self.assertEqual(Wordle.emojify(clue), '⬛⬛⬛⬛⬛', "Should be playing!")

	def test_scrambled(self):
		w = Wordle('tesla', config={'candidate_set': ['steal', 'tesla'], 'max_guesses': '6'})
		clue, state = w.guess('steal')
		self.assertEqual(state, Wordle.PLAYING, "Should be playing!")
		self.assertEqual(Wordle.emojify(clue), '🟨🟨🟨🟨🟨', "Should be wrong place!")

	def test_full_game_solved(self):
		w = Wordle('tesla', config={'candidate_set': ['steal', 'tesla', 'teals', 'unlit', 'swims', 'swabs'], 'max_guesses': '6'})
		clue, state = w.guess('steal')
		self.assertEqual(Wordle.emojify(clue), '🟨🟨🟨🟨🟨', "Should be wrong place!")
		clue, state = w.guess('swabs')
		self.assertEqual(Wordle.emojify(clue), '🟨⬛🟨⬛🟨', "Should be wrong place!")
		clue, state = w.guess('swims')
		self.assertEqual(Wordle.emojify(clue), '🟨⬛⬛⬛🟨', "Should be wrong place!")
		clue, state = w.guess('unlit')
		self.assertEqual(Wordle.emojify(clue), '⬛⬛🟨⬛🟨', "Should be wrong place!")
		clue, state = w.guess('teals')
		self.assertEqual(Wordle.emojify(clue), '🟩🟩🟨🟩🟨', "Should be wrong place!")
		clue, state = w.guess('tesla')
		self.assertEqual(Wordle.emojify(clue), '🟩🟩🟩🟩🟩', "Should be wrong place!")
		self.assertEqual(state, Wordle.SOLVED, "Should be solved!")
		# Further guesses are no-ops
		clue, state = w.guess('tesla')
		self.assertEqual(clue, None, "Clue is None!")
		self.assertEqual(state, Wordle.SOLVED, "Should be solved!")

	def test_full_game_unsolved(self):
		w = Wordle('tesla', config={'candidate_set': ['steal', 'tesla', 'teals', 'unlit', 'swims', 'swabs', 'brain'], 'max_guesses': '6'})
		clue, state = w.guess('steal')
		self.assertEqual(Wordle.emojify(clue), '🟨🟨🟨🟨🟨', "Should be wrong place!")
		clue, state = w.guess('swabs')
		self.assertEqual(Wordle.emojify(clue), '🟨⬛🟨⬛🟨', "Should be wrong place!")
		clue, state = w.guess('swims')
		self.assertEqual(Wordle.emojify(clue), '🟨⬛⬛⬛🟨', "Should be wrong place!")
		clue, state = w.guess('unlit')
		self.assertEqual(Wordle.emojify(clue), '⬛⬛🟨⬛🟨', "Should be wrong place!")
		clue, state = w.guess('teals')
		self.assertEqual(Wordle.emojify(clue), '🟩🟩🟨🟩🟨', "Should be wrong place!")
		clue, state = w.guess('brain')
		self.assertEqual(Wordle.emojify(clue), '⬛⬛🟨⬛⬛', "Should be wrong place!")
		self.assertEqual(state, Wordle.UNSOLVED, "Should be unsolved!")
		# Further guesses are no-ops
		clue, state = w.guess('tesla')
		self.assertEqual(clue, None, "Clue is None!")
		self.assertEqual(state, Wordle.UNSOLVED, "Should be solved!")


if __name__ == '__main__':
	unittest.main()