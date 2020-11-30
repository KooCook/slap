from django.db import models


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


class Genre(models.Model):
    name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


class Song(models.Model):
    title = models.CharField(max_length=289)
    lyrics = models.TextField()
    compressibility = models.FloatField()
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)
