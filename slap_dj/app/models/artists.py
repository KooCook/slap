from enum import Enum

from django.db import models

from .base import Artist, Song


class ArtistRoleInSong(Enum):
    Primary = "primary"
    Secondary = "secondary"
    Collaborator = "collaborator"
    Featured = "featured"


class ArtistInSong(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=[(tag, tag.value) for tag in ArtistRoleInSong])
