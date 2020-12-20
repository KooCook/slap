from typing import List

from django.db import models

from app_v2.models import upsert
from services.spotify import search_for_song

class Genre(models.Model):
    name = models.CharField(max_length=289)
    pretty_name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


class SpotifySong(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255, blank=False)
    track_id = models.CharField(max_length=255, unique=True,
                                blank=False)
    popularity_score = models.IntegerField()
    genres = models.ManyToManyField('Genre', unique=True)
    artist = models.ForeignKey('SpotifyArtist', null=True,
                               on_delete=models.SET_NULL)

    @classmethod
    def retrieve_song(cls, song_title: str, artists: List['Artist']):
        s = search_for_song(song_title, artists[0].name)

        instance = upsert(cls, title=s.name, track_id=s.spotify_id,
                          album_id=s.spotify_album_id, popularity_score=s.spotify_popularity)
        for genre in s.genres:
            g = upsert(Genre, name=genre)
            if cls.objects.filter(genres__name=g) > 0:
                continue
            instance.genres.add(g)
        return instance


class SpotifyArtist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255, unique=True,
                                 blank=False)
