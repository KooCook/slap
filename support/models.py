from typing import List


class SongModel:
    def __init__(self):
        self.name = ""
        self.lyrics = ""
        self.genres = []
        self.artist_names: List[str] = []
        self.compressibility = 0
        self.spotify_popularity = 0
