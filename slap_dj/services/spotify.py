from typing import List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from contract_models.spotify import SpotifySongModel, SpotifyArtistModel
from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))


def search_for_song(song_name: str, artist_name: str) -> SpotifySongModel:
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
                and artist_name.lower()
                in [a.lower() for a in artist_names]):
            s = SpotifySongModel()
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
        raise NameError(f"No such song! {song_name} : {artist_name}")
    if s is None:
        raise NameError(f"Error! {song_name} - {artist_name}")


def search_for_artists(artist_name: str) -> List[SpotifyArtistModel]:
    results = sp.search(q=f"artist:{artist_name}", type='artist', limit=20)
    artists = results['artists']['items']
    artist_contracts: List[SpotifyArtistModel] = []
    for artist in artists:
        artist_contracts.append(SpotifyArtistModel(spotify_id=artist['id']))
    return artist_contracts
