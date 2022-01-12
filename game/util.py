from collections import Counter
from typing import List
from .constants import DEFAULT_DICT, DATA_DIR
import os

def get_n_from_word_set(word_set: List[str]):
    if not len(word_set):
        raise Exception("Empty word set")
    if len(Counter([len(w) for w in word_set])) > 1:
        raise Exception("Word list must contain all same size words")
    return len(word_set[0])

from typing import List

DICT = 'data/dictionary_proper.txt'

def read_to_lines(fname: str) -> List[str]:
    with open(fname, 'r') as f:
        data = f.read()
    lines = [d for d in data.split('\n') if len(d)]
    return lines

def read_words_of_length(n: int, fname: str=DEFAULT_DICT) -> List[str]:
    if not os.path.exists(fname):
        available = []
        if os.path.exists(DATA_DIR):
            available = [os.path.join(DATA_DIR, fname) for fname in os.listdir(DATA_DIR)]
        msg = f' Pick from {available} instead in ./{DATA_DIR}/' if len(available) else ''
        raise Exception(f'Path [{fname}] does not seem to exist.{msg}')
    all_words = read_to_lines(fname)
    word_set = list(set([w for w in all_words if len(w) == n and w.islower()]))
    # Validate wordset
    get_n_from_word_set(word_set)
    return word_set