from typing import List

import numpy as np
from scipy import special

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models
from django_pandas.managers import DataFrameManager

from app.support.repetition import calculate_repetition, get_words
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
    artists = models.ManyToManyField('Artist', through='ArtistInSong')
    genres = models.ManyToManyField(Genre)
    spotify_popularity = models.IntegerField()
    objects = DataFrameManager()

    @property
    def artist_names(self) -> str:
        return ",".join([a.name for a in self.artists.all()])

    @property
    def words(self) -> List[str]:
        return list(get_words(remove_sections(self.lyrics)))

    @property
    def word_count(self) -> int:
        return len(tokenize_words(self.lyrics))

    @property
    def identifier(self) -> str:
        return f"{self.title} - {self.artist_names}"

    @property
    def weighted_popularity(self) -> float:
        """ Returns a number between 0 and 1 """
        popularity = self.spotify_popularity
        w = float(special.expit((np.log10(popularity) - 5.2) / 0.3))
        assert 0 <= w <= 1, f"weighted_popularity of {self} not in bound: {w}"
        return w

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

    @classmethod
    def upsert_video(cls, video_id: str, song: Song, **kwargs) -> 'YouTubeVideo':
        try:
            video = YouTubeVideo.objects.get(video_id=video_id)
        except ObjectDoesNotExist:
            video = YouTubeVideo(video_id=video_id, song=song, **kwargs)
            try:
                video.save()
            except IntegrityError as e:
                print(f'Fail {video.title} {song.title} - {e}')
        return video


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
