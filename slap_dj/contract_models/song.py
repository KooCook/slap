__all__ = ('SongModel', )

from dataclasses import dataclass, field
from typing import List, Iterable

from app.support.repetition import calculate_repetition
from contract_models import Artist, ArtistRole
from contract_models.genius import GeniusSongModel
from contract_models.youtube import YouTubeVideoModel
from services.genius import remove_sections
from services.spotify import search_for_song


@dataclass
class SongModel:
    name: str = ''
    lyrics: str = ''
    genres: list = field(default_factory=list)
    artists: List[Artist] = field(default_factory=list)
    compressibility: float = 0
    spotify_popularity: int = 0
    genius_id: str = ''
    spotify_id: str = ''
    spotify_album_id: str = ''
    youtube_ids: List[str] = field(default_factory=list)
    wikidata_id: str = ''
    youtube_video: YouTubeVideoModel = None
    _artist_names: str = ''

    def add_artists_from_names(self, names: List[str]):
        self.artists = [Artist(role=ArtistRole.Primary, name=name) if idx == 0
                        else Artist(role=ArtistRole.Secondary, name=name)
                        for idx, name in enumerate(names)]

    @property
    def artist_names(self) -> Iterable[str]:
        return (artist.name for artist in self.artists)

    def get_artist_by_name(self, name: str) -> Artist:
        return next(artist for artist in self.artists
                    if artist.name == name)

    @property
    def primary_artist(self) -> Artist:
        return next(artist for artist in self.artists
                    if artist.role == ArtistRole.Primary)

    def update_artists(self, artists: List[Artist]):
        names = list(self.artist_names)
        for a in artists:
            if a.name in names:
                self.get_artist_by_name(a.name).role = a.role

    def update_field_data(self):
        self.update_spotify_metadata()
        self.update_from_genius()
        self.update_repetition()

    def update_from_genius(self):
        g = GeniusSongModel.from_title_and_artist(self.name, self.primary_artist.name)
        self.genius_id = g.genius_id
        self.lyrics = g.lyrics
        print(g.artists)
        self.update_artists(g.artists)

    def update_spotify_metadata(self):
        s = search_for_song(self.name, self.primary_artist.name)
        self.spotify_popularity = s.spotify_popularity
        self.spotify_id = s.spotify_id
        self.genres = s.genres
        self.add_artists_from_names(s.artist_names)
        self.spotify_album_id = s.spotify_album_id

    def update_repetition(self):
        self.compressibility = calculate_repetition(remove_sections(self.lyrics))
