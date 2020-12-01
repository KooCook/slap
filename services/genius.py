import functools
import re
from typing import List

import lyricsgenius as lg

from settings import GENIUS_SECRET
from support.similarity_matrix import TokenizedSongLyrics

genius_client = lg.Genius(GENIUS_SECRET)


def search_for_song_lyrics(song_name: str, artist_name: str) -> str:
    song = genius_client.search_song(song_name, artist_name)
    return song.lyrics


def tokenize_words(raw_lyrics: str) -> List[str]:
    all_sections = []
    m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', raw_lyrics)
    for i in m:
        section, sub_lyrics = i
        tk = TokenizedSongLyrics(section, sub_lyrics)
        all_sections.append(tk)
    return functools.reduce(lambda x, y: x + y.tokenized if isinstance(x, list) else x.tokenized + y.tokenized, all_sections)


def clean_lyrics(sectioned: str) -> str:
    all_sections = []
    m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', sectioned)
    for i in m:
        section, sub_lyrics = i
        tk = TokenizedSongLyrics(section, sub_lyrics)
        all_sections.append(tk)
    return " ".join([s.lyrics for s in all_sections])
