from django.db import models


# Create your models here.
from services.genius import tokenize_words


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
    spotify_popularity = models.IntegerField()

    @property
    def artist_names(self) -> str:
        return ",".join([a.name for a in self.artists.all()])

    @property
    def word_count(self) -> int:
        return len(tokenize_words(self.lyrics))


class YouTubeVideo(models.Model):
    song_id = models.OneToOneField(
        Song, on_delete=models.CASCADE, primary_key=True
    )
    video_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    favorite_count = models.IntegerField()
    comment_count = models.IntegerField()
    default_language = models.CharField()
