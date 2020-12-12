from dataclasses import dataclass, field
from typing import List


@dataclass
class SongModel:
    name: str = ''
    lyrics: str = ''
    genres: list = field(default_factory=list)
    artist_names: List[str] = field(default_factory=list)
    compressibility: int = 0
    spotify_popularity: int = 0
    spotify_id: str = ''
    spotify_album_id: str = ''
