import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from support.models import SongModel

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f13fec145e594ade889c41887eb8f481",
                                                           client_secret="853c655cf5ae441cb29f3450dad900c2"))


def search_for_song(song_name: str, artist_name: str):
    results = sp.search(q=song_name, limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        genres = []
        s_name = track["name"]
        artist_names = []
        for artist in track["artists"]:
            artist = sp.artist(artist["external_urls"]["spotify"])
            genres.extend(artist["genres"])
            artist_names.append(artist["name"])
        if s_name == song_name and artist_name in artist_names:
            s = SongModel()
            s.genres = genres
            s.name = song_name
            s.artist_name = artist_name
            return s
        print("track genres:", genres)
        # print(track)
