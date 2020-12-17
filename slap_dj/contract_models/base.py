from dataclasses import dataclass, field
from typing import List

from app.support.repetition import calculate_repetition
from services.genius import search_for_song_lyrics, remove_sections
from services.spotify import search_for_song

__all__ = ('SongModel', )


@dataclass
class SongModel:
    name: str = ''
    lyrics: str = ''
    genres: list = field(default_factory=list)
    artist_names: List[str] = field(default_factory=list)
    compressibility: float = 0
    spotify_popularity: int = 0
    spotify_id: str = ''
    spotify_album_id: str = ''
    youtube_ids: List[str] = field(default_factory=list)
    wikidata_id: str = ''

    @property
    def combined_artist_names(self) -> str:
        return self.artist_names[0]

    def update_field_data(self):
        self.update_lyrics()
        self.update_spotify_metadata()
        self.update_repetition()

    def update_lyrics(self):
        self.lyrics = search_for_song_lyrics(self.name, self.combined_artist_names)

    def update_spotify_metadata(self):
        s = search_for_song(self.name, self.combined_artist_names)
        self.spotify_popularity = s.spotify_popularity
        self.spotify_id = s.spotify_id
        self.genres = s.genres
        self.artist_names = s.artist_names
        self.spotify_album_id = s.spotify_album_id

    def update_repetition(self):
        self.compressibility = calculate_repetition(remove_sections(self.lyrics))
