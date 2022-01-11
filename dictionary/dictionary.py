from typing import List

DICT = 'data/dictionary_proper.txt'

def read_to_lines(fname: str) -> List[str]:
	with open(fname, 'r') as f:
		data = f.read()
	lines = [d for d in data.split('\n') if len(d)]
	return lines

def read_words_of_length(n: int) -> List[str]:
	all_words = read_to_lines(DICT)
	return [w for w in all_words if len(w) == n]