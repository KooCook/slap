import re

import lyricsgenius as lg

from support.similarity_matrix import TokenizedSongLyrics

genius_client = lg.Genius("cLdigwShk0dtga_4LwuaX5FoNW-j1T-0X37ucmzmGuo2Dlm53yC6FO1keQ7BGQKe")


def search_for_song_lyrics(song_name: str, artist_name: str) -> str:
    song = genius_client.search_song(song_name, artist_name)
    return song.lyrics


def clean_lyrics(sectioned: str) -> str:
    all_sections = []
    m = re.findall(r'\[(.+)\][ \n]+([^\[]+)', sectioned)
    for i in m:
        section, sub_lyrics = i
        tk = TokenizedSongLyrics(section, sub_lyrics)
        all_sections.append(tk)
    return " ".join([s.lyrics for s in all_sections])
