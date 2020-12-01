import functools
import string
from itertools import product
import re
from typing import List

from nltk import word_tokenize
# from nltk.tokenize import WhitespaceTokenizer
import numpy as np

from support.init.nltk import initialize_nltk
from nltk.tokenize import TweetTokenizer

initialize_nltk()

lyrics = """
[Intro]
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Ra-ra-ah-ah-ah
Roma Roma-ma
Gaga, "Ooh la-la"
Want your bad romance
Ra-ra-ah-ah-ah
Roma, Roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Verse 1]
I want your ugly, I want your disease
I want your everything as long as it’s free
I want your love
Love, love, love, I want your love, oh, ey
I want your drama, the touch of your hand (Hey!)
I want your leather-studded kiss in the sand
I want your love
Love, love, love, I want your love
(Love, love, love, I want your love)

[Pre-Chorus]
You know that I want you
And you know that I need you
I want it bad
Your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Verse 2]
I want your horror, I want your design
‘Cause you’re a criminal as long as you’re mine
I want your love
Love, love, love, I want your love, uh
I want your psycho, your vertigo shtick (Shtick, hey!)
Want you in my rear window, baby, you're sick
I want your love
Love, love, love, I want your love
(Love, love, love, I want your love)

[Pre-Chorus]
You know that I want you
And you know that I need you (
'Cause I'm a free bitch, baby
)
I want it bad
Your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Bridge 1]
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, passion, baby
Work it, I'm a free bitch, baby

[Bridge 2]
I want your love, and I want your revenge
I want your love, I don't wanna be friends
Je veux ton amour et je veux ta revanche
Je veux ton amour, I don't wanna be friends
(Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh)
(I want you back) No, I don't wanna be friends
(Caught in a bad romance) I don't wanna be friends
Want your bad romance
(Caught in a bad romance) Want your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
(Want your bad romance)
Caught in a bad romance (Want your bad romance)
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
(Want your bad romance)
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma, Roma-ma
Gaga, "Ooh la-la"
Want your bad romance
"""


class TokenizedSongLyrics:
    def __init__(self, section: str, lyrics: str):
        self.section = section
        self.lyrics = lyrics

    @property
    def tokenized(self) -> List[str]:
        words = TweetTokenizer().tokenize(self.lyrics)
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


all_sections = []
m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', lyrics)
for i in m:
    section, sub_lyrics = i
    tk = TokenizedSongLyrics(section, sub_lyrics)
    all_sections.append(tk)

all_lyrics = functools.reduce(lambda x, y: x + y.tokenized if isinstance(x, list) else x.tokenized + y.tokenized, all_sections)

if __name__ == '__main__':
    print(get_similarity_matrix(all_lyrics))
