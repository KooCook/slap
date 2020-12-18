from app.support.repetition import calculate_repetition
from contract_models.genius import GeniusSongModel
from .genius import clean_lyrics, remove_sections
from .spotify import search_for_song
from contract_models.song import SongModel


def generate_song_to_model(song_name, song_artist) -> SongModel:
    song_artist = song_artist.split(" Featuring")[0]
    s = search_for_song(song_name, song_artist)
    s.lyrics = GeniusSongModel.from_song_artist(s.name, song_artist).lyrics
    if s.lyrics:
        lyrics = remove_sections(s.lyrics)
        s.compressibility = calculate_repetition(lyrics)
    s.genres = s.genres
    return s
