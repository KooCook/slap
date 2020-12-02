from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from repetition import calculate_repetition
from services.genius import remove_sections

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
    spotify_popularity = models.IntegerField()

    @property
    def artist_names(self) -> str:
        return ",".join([a.name for a in self.artists.all()])

    def update_compression_ratio(self):
        new = calculate_repetition(remove_sections(self.lyrics))
        print(f"Updating model {self}\n"
              f"old: {self.compressibility}\n"
              f"new: {new}")
        self.compressibility = new
        self.save()


class YouTubeVideo(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    favorite_count = models.IntegerField()
    comment_count = models.IntegerField()
    default_language = models.CharField(max_length=10)


class BillboardYearEndEntry(models.Model):
    chart = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    rank = models.IntegerField()
    song = models.OneToOneField(Song, on_delete=models.CASCADE)

    @classmethod
    def from_dict(cls, dct: dict, song: Song) -> 'BillboardYearEndEntry':
        try:
            entry = cls.objects.get(song=song)
            return entry
        except cls.DoesNotExist:
            chart = dct['chart']
            year = dct['year']
            rank = dct['rank']
            title = dct['title']
            artist = dct['artist']
            image_url = dct['image']
            entry = cls(chart=chart, year=year, rank=rank,
                        title=title, artist=artist,
                        image_url=image_url, song=song)
            return entry


class SpotifyTrack(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255)
