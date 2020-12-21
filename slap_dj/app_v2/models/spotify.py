from typing import List, Iterable

from django.db import models

from app_v2.db.utils import upsert
from contract_models.spotify import SpotifySongModel
from services.spotify import search_for_song


class Genre(models.Model):
    name = models.CharField(max_length=289)
    pretty_name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


def retrieve_from_song_title_and_possible_artists(song_title: str, possible_artist_names: Iterable[str]) -> List['SpotifySong']:
    songs = []
    for name in possible_artist_names:
        try:
            s = search_for_song(song_title, name)
        except NameError:
            continue
        if s is None:
            continue
        song = SpotifySong.from_song_model(s)
        for artist in s.artists:
            artist_obj = upsert(SpotifyArtist, name=artist.name, artist_id=artist.spotify_id)
            song.artists.add(artist_obj)
        songs.append(song)
    return songs


class SpotifySong(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255, blank=False)
    track_id = models.CharField(max_length=255, unique=True,
                                blank=False)
    popularity_score = models.IntegerField()
    genres = models.ManyToManyField('Genre')
    artists = models.ManyToManyField('SpotifyArtist')

    @classmethod
    def from_song_model(cls, s: SpotifySongModel):
        if s is None:
            raise TypeError("'s' should be a SpotifySongModel, not None")
        instance = upsert(cls,
                          title=s.name,
                          track_id=s.spotify_id,
                          album_id=s.spotify_album_id,
                          popularity_score=s.spotify_popularity,
                          )
        for genre in s.genres:
            g = upsert(Genre, name=genre)
            instance.genres.add(g)
        return instance

    @classmethod
    def retrieve_song(cls, song_title: str, artists_names: List[str]) -> 'SpotifySong':
        # Ensure that it at least has an ID
        s = search_for_song(song_title, artists_names[0])
        return cls.from_song_model(s)


class SpotifyArtist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255, unique=True,
                                 blank=False)
