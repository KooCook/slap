from typing import List

from django.db import models
from django_pandas.managers import DataFrameManager

from app.support.repetition import calculate_repetition
from services.genius import remove_sections, tokenize_words


__all__ = ['Genre', 'Song', 'YouTubeVideo',
           'BillboardYearEndEntry', 'SpotifyTrack', 'SpotifySongWeeklyStream']


class Genre(models.Model):
    name = models.CharField(max_length=289)
    pretty_name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}


class Song(models.Model):
    title = models.CharField(max_length=289)
    lyrics = models.TextField()
    compressibility = models.FloatField()
    artists = models.ManyToManyField(Artist, through='ArtistInSong')
    genres = models.ManyToManyField(Genre)
    spotify_popularity = models.IntegerField()
    objects = DataFrameManager()

    @property
    def artist_names(self) -> str:
        return ",".join([a.name for a in self.artists.all()])

    @property
    def words(self) -> List[str]:
        return tokenize_words(self.lyrics)

    @property
    def word_count(self) -> int:
        return len(tokenize_words(self.lyrics))

    @property
    def identifier(self) -> str:
        return f"{self.title} - {self.artist_names}"

    def update_compression_ratio(self):
        new = calculate_repetition(remove_sections(self.lyrics))
        print(f"Updating model {self}\n"
              f"old: {self.compressibility}\n"
              f"new: {new}")
        self.compressibility = new
        self.save()


class YouTubeVideo(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    dislike_count = models.BigIntegerField()
    favorite_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    default_language = models.CharField(max_length=10, null=True)
    published_at = models.DateTimeField(null=True)
    channel_title = models.CharField(max_length=255, null=True)


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


class SpotifySongWeeklyStream(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    streams = models.BigIntegerField()
    week_date = models.CharField(max_length=255)
