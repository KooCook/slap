from typing import List, Optional

import numpy as np
from django.db import models
from django.db.models.aggregates import Min, Max
from scipy import special

from app.support.repetition import get_bow_dataframe
from app_v2.db.utils import upsert


class Song(models.Model):
    # youtube_videos = models.OneToManyField('YoutubeVideo', null=True, on_delete=models.SET_NULL)
    genius_song = models.OneToOneField('GeniusSong', null=True, on_delete=models.SET_NULL)
    wikidata_song = models.OneToOneField('WikidataSong', null=True, on_delete=models.SET_NULL)
    spotify_song = models.OneToOneField('SpotifySong', null=True, on_delete=models.SET_NULL)
    artists = models.ManyToManyField('Artist', through='ArtistSong')
    # cached fields
    compressibility = models.FloatField(null=True)

    @property
    def title(self) -> str:
        if self.wikidata_song:
            if self.wikidata_song.title:
                return self.wikidata_song.title
        if self.genius_song:
            if self.genius_song.title:
                return self.genius_song.title
        if self.spotify_song:
            if self.spotify_song.title:
                return self.spotify_song.title
        raise ValueError("No title available for this Song.")

    @property
    def artists_names(self) -> List[str]:
        return list(map(lambda a: a.name, self.artists.all()))

    @property
    def weighted_popularity(self) -> Optional[float]:
        """ Returns a number between 0 and 1 if popularity exists."""

        yt_vids = self.youtube_videos.all()
        if len(yt_vids) == 0:
            raise ValueError("No youtube videos available")

        # strategy = max view_count
        popularity = max(map(lambda x: x.view_count, yt_vids))

        if popularity:
            w = float(special.expit((np.log10(popularity) - 5.2) / 0.3))
            assert 0 <= w <= 1, f"weighted_popularity of {self} not in bound: {w}"
            return w
        else:
            raise ValueError("The view count does not exist.")

    def link_to_wikidata(self):
        from app_v2.models.wikidata import WikidataSong
        if self.wikidata_song is not None:
            # already linked
            return
        wd_song = WikidataSong.retrieve_song(self.title, self.artists_names)
        self.wikidata_song = wd_song
        self.save()

    def link_to_spotify(self):
        from app_v2.models.spotify import SpotifySong
        if self.spotify_song is not None:
            # already linked
            return
        spotify_song = SpotifySong.retrieve_song(self.title, [self.artists.first().name])
        self.spotify_song = spotify_song
        self.save()

    def link_to_genius(self):
        from app_v2.models.genius import GeniusSong
        if self.genius_song is not None:
            # already linked
            return
        # Use spotify title bc service is related
        genius_song = GeniusSong.retrieve_song(self.spotify_song.title, [self.artists.first().name])
        self.genius_song = genius_song
        self.save()


class ArtistSong(models.Model):
    class Role(models.TextChoices):
        Primary = "primary"
        Secondary = "secondary"
        Collaborator = "collaborator"
        Featured = "featured"

    class Meta:
        unique_together = ('artist', 'song')

    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=Role.choices)

    @classmethod
    def upsert(cls, song: Song, artist: 'Artist'):
        try:
            return cls.objects.get(song=song, artist=artist)
        except cls.DoesNotExist:
            inst = cls(song=song, artist=artist)
            inst.save()
            return inst


class Word(models.Model):
    word = models.CharField(max_length=289, unique=True)
    occurs_in_song = models.ManyToManyField('Song', through='WordSong')
    popularity_score = models.FloatField(null=True)

    # wordoccurrenceinsong_set from ManyToManyField
    @classmethod
    def min_relative_popularity(cls) -> float:
        return cls.objects.aggregate(Min('popularity_score'))['popularity_score__min']

    # compared to max
    @classmethod
    def max_popularity(cls) -> float:
        s = cls.objects.aggregate(Max('popularity_score'))
        return s['popularity_score__max']

    @property
    def relative_popularity(self) -> float:
        if not self.popularity_score:
            return 0
        return self.popularity_score / self.max_popularity()

    def update_popularity(self):
        self.popularity_score = self.get_popularity()
        self.save()

    def get_popularity(self) -> float:
        word_occurrence_in_songs = self.wordsong_set.all()
        lst = []
        for ws in word_occurrence_in_songs:
            try:
                lst.append(ws.weighted_frequency * ws.appears_in.weighted_popularity)
            except models.base.ObjectDoesNotExist:
                pass
        return sum(lst)


class WordSong(models.Model):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    frequency = models.IntegerField()
    section = models.CharField(max_length=50)

    @property
    def weighted_frequency(self, ) -> float:
        """ Returns a number between 0 and 1 """
        w = float(special.expit(self.frequency - 2.8))
        assert 0 <= w <= 1, f"weighted_frequency of {self} not in bound: {w}"
        return w

    @classmethod
    def update_all_songs_word_frequency(cls, skip: bool = True) -> None:
        for song in cls.objects.all():
            try:
                occurrence = cls.objects.filter(appears_in=song)
                if skip and len(occurrence) > 0:
                    print(f"skip {song.id} {song.title}")
                    continue
            except cls.DoesNotExist:
                pass
            cls.update_song_word_frequency(song)
            print(f"freq {song.title}")

    @classmethod
    def update_song_word_frequency(cls, song: Song) -> None:
        df = get_bow_dataframe(song.genius_song.words)
        freq = df['freq']
        words = df['word']
        for w, f in zip(words, freq):
            upsert(cls, word=w, song=song, frequency=f)


class Artist(models.Model):
    wikidata_artist = models.OneToOneField('WikidataArtist', null=True, on_delete=models.SET_NULL)
    genius_artist = models.OneToOneField('GeniusArtist', null=True, on_delete=models.SET_NULL)
    spotify_artist = models.OneToOneField('SpotifyArtist', null=True, on_delete=models.SET_NULL)
    youtube_channels = models.OneToOneField('YoutubeChannel', null=True, on_delete=models.SET_NULL)

    @property
    def name(self) -> str:
        if self.wikidata_artist:
            if self.wikidata_artist:
                return self.wikidata_artist.name
        if self.genius_artist:
            if self.wikidata_artist:
                return self.genius_artist.name
        if self.spotify_artist:
            if self.spotify_artist.name:
                return self.spotify_artist.name
        raise ValueError("No name available for this Artist.")

    def link_to_spotify(self):
        if self.spotify_artist is not None:
            # already linked
            return

    def link_to_wikidata(self):
        if self.wikidata_artist is not None:
            # already linked
            return
        # WikidataArtist.
        # wiki_artist
