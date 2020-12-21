from typing import List

from django.db import models

from app_v2.db.utils import upsert
from contract_models.spotify import SpotifySongModel
from services.spotify import search_for_song


class Genre(models.Model):
    name = models.CharField(max_length=289)
    pretty_name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


def retrieve_from_song_title_and_possible_artists(song_title: str, possible_artist_names: List[str]) -> List['SpotifySong']:
    songs = []
    for artist in possible_artist_names:
        try:
            s = search_for_song(song_title, artist)
        except NameError:
            continue
        song = SpotifySong.from_song_model(s)
        song.artist = SpotifySong
        # TODO: Create artist from this and connect to Song
        songs.append()
    return songs


class SpotifySong(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255, blank=False)
    track_id = models.CharField(max_length=255, unique=True,
                                blank=False)
    popularity_score = models.IntegerField()
    genres = models.ManyToManyField('Genre')
    artist = models.ForeignKey('SpotifyArtist', null=True,
                               on_delete=models.SET_NULL)

    @classmethod
    def from_song_model(cls, s: SpotifySongModel):
        instance = upsert(cls, title=s.name, track_id=s.spotify_id,
                          album_id=s.spotify_album_id, popularity_score=s.spotify_popularity)
        for genre in s.genres:
            g = upsert(Genre, name=genre)
            if cls.objects.filter(genres__name=g) > 0:
                continue
            instance.genres.add(g)
        return instance

    @classmethod
    def retrieve_song(cls, song_title: str, artists: List['Artist']) -> 'SpotifySong':
        s = search_for_song(song_title, artists[0].name)
        return cls.from_song_model(s)



class SpotifyArtist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255, unique=True,
                                 blank=False)
