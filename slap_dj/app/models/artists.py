from django.db import models

from services.wikidata import get_artist_akas
from .base import Song


__all__ = ['Artist', 'ArtistAkas', 'ArtistInSong']


class Artist(models.Model):
    name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}

    def generate_akas(self):
        for akas in get_artist_akas(self.name):
            ArtistAkas(artist=self, name=akas).save()


class ArtistAkas(models.Model):
    name = models.CharField(max_length=150, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class ArtistInSong(models.Model):

    class Role(models.TextChoices):
        Primary = "primary"
        Secondary = "secondary"
        Collaborator = "collaborator"
        Featured = "featured"

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=Role.choices)
