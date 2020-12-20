from django.db import models

from app_v2.models import upsert, Artist
from contract_models.genius import GeniusSongModel


class GeniusSong(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField()
    song_id = models.CharField(max_length=15, unique=True,
                               blank=False)

    @classmethod
    def retrieve_song(cls, title, artists) -> 'GeniusSong':
        s = GeniusSongModel.from_title_and_artist(title, artists)
        return upsert(cls, title=s.title,
                      lyrics=s.lyrics,
                      song_id=s.genius_id)


class GeniusArtist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=15, unique=True,
                               blank=False)
