from typing import List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from app.support.models import SongModel

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))


def search_for_song(song_name: str, artist_name: str) -> SongModel:
    results = sp.search(q=f"artist:{artist_name} track:{song_name}", type='track', limit=20)
    s = None
    items = results['tracks']['items']
    for idx, track in enumerate(items):
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
            s.spotify_popularity = track["popularity"]
            s.spotify_id = track["id"]
            s.spotify_album_id = track["album"]["id"]
            return s
        else:
            continue
    if len(items) == 0:
        raise Exception(f"No such song! {song_name} : {artist_name}")
    if s is None:
        raise Exception(f"Error! {song_name} - {artist_name}")
