from typing import List

import numpy as np
from django.db.models.aggregates import Sum
from scipy import special

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models
from django_pandas.managers import DataFrameManager

from app.support.repetition import calculate_repetition, get_words
from contract_models.song import SongModel
from contract_models.youtube import YouTubeVideoModel
from services.genius import remove_sections, tokenize_words

__all__ = ['Genre', 'Song', 'YouTubeVideo',
           'BillboardYearEndEntry', 'SpotifyTrack', 'SpotifySongWeeklyStream']

from services.wikidata import retrieve_songmodel_wikidata


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
    wikidata_id = models.CharField(max_length=13)
    genius_id = models.CharField(max_length=15)
    # image_url = models.URLField()
    objects = DataFrameManager()

    def retrieve_wikidata_id(self):
        """ Retrieves wikidata from title, artist
        genre? """
        if self.wikidata_id:
            return
        aw_ids = [a.wikidata_id for a in self.artists]
        song: SongModel = retrieve_songmodel_wikidata(song_title=self.title, artists=aw_ids)
        self.wikidata_id = song.wikidata_id
        self.save()

    @property
    def artist_names(self) -> str:
        return ",".join([a.title for a in self.artists.all()])

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
        popularity = list(self.youtubevideo_set.all())[0].view_count
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
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    # song = models.OneToOneField(Song, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255, unique=True,
                                blank=False)
    title = models.CharField(max_length=255, null=True)
    view_count = models.BigIntegerField(null=True)
    like_count = models.BigIntegerField(null=True)
    dislike_count = models.BigIntegerField(null=True)
    favorite_count = models.BigIntegerField(null=True)
    comment_count = models.BigIntegerField(null=True)
    default_language = models.CharField(max_length=10, null=True)
    published_at = models.DateTimeField(null=True)
    channel_title = models.CharField(max_length=255, null=True)
    channel_id = models.CharField(max_length=255, null=True)

    @classmethod
    def update_all_video_stats(cls, start = 0):
        all_vid_count = cls.objects.all().count()
        current = start
        while current < all_vid_count:
            models = YouTubeVideoModel.from_video_ids(list(dct['video_id'] for dct in cls.objects.all()[current:current + 50].values('video_id')))
            for m in models:
                inst = cls.objects.get(video_id=m.video_id)
                inst.update_stats(m)
            current += current + YouTubeVideoModel.HARD_LIMIT

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
        # video.update_stats()
        return video

    def update_stats(self, yt_video = None):
        if yt_video is None:
            yt_video = YouTubeVideoModel.from_video_id(self.video_id)
        if not self.title:
            self.title = yt_video.title
        self.view_count = yt_video.view_count
        self.like_count = yt_video.like_count
        self.favorite_count = yt_video.favorite_count
        self.dislike_count = yt_video.dislike_count
        self.comment_count = yt_video.comment_count
        self.published_at = yt_video.published_at
        self.channel_title = yt_video.channel_title
        self.channel_id = yt_video.channel_id
        self.default_language = yt_video.default_language
        self.save()


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
    track_id = models.CharField(max_length=255, unique=True)
    album_id = models.CharField(max_length=255)

    @classmethod
    def upsert(cls, track_id: str, song: Song, **kwargs) -> 'YouTubeVideo':
        try:
            video = cls.objects.get(track_id=track_id)
        except ObjectDoesNotExist:
            video = cls(track_id=track_id, song=song, **kwargs)
            try:
                video.save()
            except IntegrityError as e:
                print(f'Fail {video.track_id} {song.title} - {e}')
        return video


class SpotifySongWeeklyStream(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    streams = models.BigIntegerField()
    week_date = models.CharField(max_length=255)
