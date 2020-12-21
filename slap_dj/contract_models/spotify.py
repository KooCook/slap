from dataclasses import dataclass, field
from typing import List


@dataclass
class SpotifySongModel:
    name: str = ''
    genres: list = field(default_factory=list)
    artists: List['SpotifyArtistModel'] = field(default_factory=list)
    artist_names: List[str] = field(default_factory=list)
    spotify_popularity: int = 0
    spotify_id: str = ''
    spotify_album_id: str = ''
    wikidata_id: str = ''


@dataclass
class SpotifyArtistModel:
    spotify_id: str = ''
    name: str = ''
    genres: list = field(default_factory=list)
    popularity: int = 0
