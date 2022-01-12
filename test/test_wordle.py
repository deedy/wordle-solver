import unittest
from game.wordle import Wordle

class TestWordle(unittest.TestCase):

	def test_invalid_word_list(self):
		with self.assertRaises(Exception) as context:
			w = Wordle(['gorge', 'gorges'], 'gorge')
		with self.assertRaises(Exception) as context:
			w = Wordle([], 'gorge')

	def test_solved(self):
		w = Wordle(['gorge'], 'gorge')
		clue, state = w.guess('gorge')
		self.assertEqual(state, Wordle.SOLVED, "Should be solved!")
		self.assertEqual(Wordle.emojify(clue), '🟩🟩🟩🟩🟩', "Should be solved!")

	def test_missed_all(self):
		w = Wordle(['gorge', 'unlit'], 'gorge')
		clue, state = w.guess('unlit')
		self.assertEqual(state, Wordle.PLAYING, "Should be playing!")
		self.assertEqual(Wordle.emojify(clue), '⬛⬛⬛⬛⬛', "Should be playing!")

	def test_scrambled(self):
		w = Wordle(['steal', 'tesla'], 'tesla')
		clue, state = w.guess('steal')
		self.assertEqual(state, Wordle.PLAYING, "Should be playing!")
		self.assertEqual(Wordle.emojify(clue), '🟨🟨🟨🟨🟨', "Should be wrong place!")

	def test_full_game_solved(self):
		w = Wordle(['steal', 'tesla', 'teals', 'unlit', 'swims', 'swabs'], 'tesla')
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
		w = Wordle(['steal', 'tesla', 'teals', 'unlit', 'swims', 'swabs', 'brain'], 'tesla')
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