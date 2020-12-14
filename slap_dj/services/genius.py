import functools
import re
from typing import List

import lyricsgenius as lg
from nltk import TweetTokenizer

from settings import GENIUS_SECRET
from app.support.similarity_matrix import TokenizedSongLyrics
from utils.iter import remove_consecs

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
    return functools.reduce(lambda x, y: x + y.tokenized, all_sections, [])


def tokenize_words_simple(raw_words: str) -> List[str]:
    return TweetTokenizer().tokenize(raw_words)


def clean_lyrics(sectioned: str) -> str:
    all_sections = []
    m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', sectioned)
    for i in m:
        section, sub_lyrics = i
        tk = TokenizedSongLyrics(section, sub_lyrics)
        all_sections.append(tk)
    return " ".join([s.lyrics for s in all_sections])


def remove_sections(raw_lyrics: str) -> str:
    """Returns lyrics with the sections removed."""
    lines = raw_lyrics.splitlines(keepends=True)
    cleaned_lines = [line for line in lines if re.match(f'^\[.*]\\n?$', line) is None]
    cleaned_text = ''.join(remove_consecs(cleaned_lines, '\n'))
    return cleaned_text.rstrip() + '\n'
