from typing import List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from support.models import SongModel

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f13fec145e594ade889c41887eb8f481",
                                                           client_secret="853c655cf5ae441cb29f3450dad900c2"))


def search_for_song(song_name: str, artist_name: str):
    results = sp.search(q=song_name, type='track', limit=20)
    s = None
    for idx, track in enumerate(results['tracks']['items']):
        genres = []
        s_name = track["name"]
        artist_names: List[str] = []
        for artist in track["artists"]:
            artist = sp.artist(artist["external_urls"]["spotify"])
            genres.extend(artist["genres"])
            artist_names.append(artist["name"])
        if (s_name.lower() == song_name.lower()
                and artist_name.lower() in [a.lower() for a in artist_names]):
            s = SongModel()
            s.genres = genres
            s.name = s_name
            s.artist_names = artist_names
            return s
        else:
            continue
    if s is None:
        raise Exception("Error!")
