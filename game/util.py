from collections import Counter
from typing import List

def get_n_from_word_set(word_set: List[str]):
    if not len(word_set):
        raise Exception("Empty word set")
    if len(Counter([len(w) for w in word_set])) > 1:
        raise Exception("Word list must contain all same size words")
    return len(word_set[0])