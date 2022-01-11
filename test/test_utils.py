import unittest
from game.solver.util import indexall, is_guessable_word

class TestUtils(unittest.TestCase):

	def test_indexall(self):
		ixes = indexall('gorge', 'g')
		self.assertEqual(ixes, set([0, 3]), "Multiple ixes")
		ixes = indexall('gorge', 'o')
		self.assertEqual(ixes, set([1]), "Single ixes")
		ixes = indexall('gorge', 'r')
		self.assertEqual(ixes, set([2]), "Single ixes")
		ixes = indexall('gorge', 'e')
		self.assertEqual(ixes, set([4]), "Single ixes")
		ixes = indexall('gorge', 'a')
		self.assertEqual(ixes, set([]), "No match")

	def test_is_guessable_word_not_in_word(self):	
		is_guessable = is_guessable_word('tesla', {}, {}, set('abcd'))
		self.assertFalse(is_guessable)
		is_guessable = is_guessable_word('tesla', {}, {}, set('bcdfghijkmnopqruvwxyz'))
		self.assertTrue(is_guessable)

	def test_is_guessable_word_in_word_wrong_place(self):	
		is_guessable = is_guessable_word('tesla', {}, {'s': set([2])}, {})
		self.assertFalse(is_guessable)
		is_guessable = is_guessable_word('tesla', {}, {'s': set([0, 1, 3, 4])}, {})
		self.assertTrue(is_guessable)
		is_guessable = is_guessable_word('tesla', {}, {'t': set([0]), 'e': set([2])}, {})
		self.assertFalse(is_guessable)
		is_guessable = is_guessable_word('tesla', {}, {'t': set([1, 2, 3, 4]), 'e': set([0, 2, 3, 4])}, {})
		self.assertTrue(is_guessable)

	def test_is_guessable_word_in_word_right_place(self):	
		is_guessable = is_guessable_word('tesla', {'t': set([1, 2, 3, 4])}, {}, {})
		self.assertFalse(is_guessable)
		is_guessable = is_guessable_word('tesla', {'t': set([0]), 'e': set([1]), 's': set([2]), 'l': set([3]), 'a': set([4])}, {}, {})
		self.assertTrue(is_guessable)


if __name__ == '__main__':
	unittest.main()