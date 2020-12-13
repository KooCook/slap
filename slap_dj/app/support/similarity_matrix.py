import random
import string
from itertools import product
from typing import List, Dict
# from nltk.tokenize import WhitespaceTokenizer
import numpy as np

from app.support.repetition import get_bow_dataframe, get_words
from app.support.init.nltk import initialize_nltk

initialize_nltk()


class TokenizedSongLyrics:
    def __init__(self, section: str, lyrics: str):
        self.section = section
        self.lyrics = lyrics

    @property
    def tokenized(self) -> List[str]:
        # TweetTokenizer().tokenize(self.lyrics)
        words = get_words(self.lyrics)
        return [word for word in words if word not in string.punctuation]

    def __repr__(self):
        return f"SongLyrics<'{self.section}', l={self.lyrics[:20]}...>"


def get_similarity_matrix(lst: list) -> np.ndarray:
    size = len(lst)
    p = list(product(lst, lst))
    q = list(map(lambda x: x[0] == x[1], p))
    u = np.asarray(q)
    return np.reshape(u, (size, size))


def get_similarity_matrix_map(words: list):
    lst = list(range(len(words)))
    p = list(product(lst, lst))
    q = list(map(lambda x: (x[0], x[1], 50) if words[x[0]] == words[x[1]] else (x[0], x[1], 0), p))
    return q


def get_words_with_colors(words: List[str]) -> Dict[str, str]:
    bow = get_bow_dataframe(words)
    bow_lst = bow['word'].values.tolist()
    r = lambda: random.randint(0, 255)
    dct = {x: '#%02X%02X%02X' % (r(), r(), r()) for x in bow_lst}
    return dct


def get_similarity_matrix_map_v2(words: list):
    lst = list(range(len(words)))
    p = list(product(lst, lst))
    color_map = get_words_with_colors(words)
    q = list((x[0], x[1], words[x[0]], color_map[words[x[0]].lower()]) for x in p if words[x[0]].lower() == words[x[1]].lower())
    return q
