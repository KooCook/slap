import functools
from itertools import product
import re

from nltk import word_tokenize
import numpy as np

from support.init.nltk import initialize_nltk

initialize_nltk()
lyrics = """
[Verse 1]
I'm so into you, I can barely breathe
And all I wanna do is to fall in deep
But close ain't close enough 'til we cross the line, hey yeah
So name a game to play and I'll roll the dice, hey

[Pre-Chorus]
Oh baby, look what you started
The temperature's rising in here
Is this gonna happen?
Been waiting and waiting for you to make a move
Before I make a move

[Chorus]
So, baby, come light me up, and, baby, I'll let you on it
A little bit dangerous, but, baby, that's how I want it
A little less conversation and a little more touch my body
'Cause I'm so into you, into you, into you
Got everyone watchin' us, so, baby, let's keep this secret
A little bit scandalous, but, baby, don't let them see it
A little less conversation and a little more touch my body
'Cause I'm so into you, into you, into you (Ooh, yeah)

[Verse 2]
This could take some time, hey
Made too many mistakes
Better get this right, right, baby

[Pre-Chorus]
Oh, baby, look what you started
The temperature's rising in here
Is this gonna happen?
Been waiting and waiting for you to make a move
Before I make a move

[Chorus]
So, baby, come light me up, and, baby, I'll let you on it
A little bit dangerous, but, baby, that's how I want it
A little less conversation and a little more touch my body
'Cause I'm so into you, into you, into you
Got everyone watchin' us, so, baby, let's keep this secret
A little bit scandalous, but, baby, don't let them see it
A little less conversation and a, little more touch my body
'Cause I'm so into you, into you, into you, oh yeah
('Cause I'm so into you)

[Bridge]
Tell me what you came here for
'Cause I can't, I can't wait no more
I'm on the edge with no control
And I need, I need you to know
You to know, oh, woah, yeah

[Chorus]
So, baby, come light me up (Light me up), and, baby, I'll let you on it
A little bit dangerous (Dangerous), but, baby, that's how I want it (How I want it)
A little less conversation and a little more touch my body
'Cause I'm so into you, into you, into you
Got everyone watchin' us (Watchin' us), so, baby, let's keep this secret
A little bit scandalous (Scandalous), but, baby, don't let them see it (Yeah)
A little less conversation  and a little more touch my body
'Cause I'm so into you, into you, into you

[Outro]
So come light me up
So come light me up, my baby
Little dangerous
A little dangerous, my boy (How I want it)
A little less conversation and a little more touch my body
'Cause I'm so into you, into you, into you
(I'm so into you)
"""


class TokenizedSongLyrics:
    def __init__(self, section: str, lyrics: str):
        self.section = section
        self.lyrics = lyrics

    @property
    def tokenized(self):
        words = word_tokenize(self.lyrics)
        return [word for word in words if word.isalnum()]

    def __repr__(self):
        return f"SongLyrics<'{self.section}', l={self.lyrics[:20]}...>"


def get_similarity_matrix(lst: list) -> np.ndarray:
    size = len(lst)
    p = list(product(lst, lst))
    q = list(map(lambda x: x[0] == x[1], p))
    u = np.asarray(q)
    return np.reshape(u, (size, size))


all_sections = []
m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', lyrics)
for i in m:
    section, sub_lyrics = i
    tk = TokenizedSongLyrics(section, sub_lyrics)
    all_sections.append(tk)

if __name__ == '__main__':
    all_lyrics = functools.reduce(lambda x, y: x + y.tokenized if isinstance(x, list) else x.tokenized + y.tokenized, all_sections)
    print(get_similarity_matrix(all_lyrics))
