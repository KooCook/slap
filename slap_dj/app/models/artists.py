from django.db import models

from .base import Artist, Song


__all__ = ['Artist', 'Song']


class ArtistInSong(models.Model):

    class Role(models.TextChoices):
        Primary = "primary"
        Secondary = "secondary"
        Collaborator = "collaborator"
        Featured = "featured"

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=Role.choices)
