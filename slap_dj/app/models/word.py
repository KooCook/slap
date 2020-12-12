from django.db import models

from repetition import get_bow_dataframe
from .base import Song


__all__ = ['WordCache', 'WordOccurrenceInSong']


class WordCache(models.Model):
    word = models.CharField(max_length=289, unique=True)
    occurs_in_song = models.ManyToManyField(Song, through='WordOccurrenceInSong')


class WordOccurrenceInSong(models.Model):
    word = models.ForeignKey(WordCache, on_delete=models.CASCADE)
    appears_in = models.ForeignKey(Song, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    @classmethod
    def update_all_songs_word_frequency(cls, skip: bool = True) -> None:
        for song in Song.objects.all():
            try:
                occurrence = cls.objects.filter(appears_in=song)
                if skip and occurrence is not None:
                    continue
            except cls.DoesNotExist:
                pass
            cls.update_song_word_frequency(song)

    @classmethod
    def update_song_word_frequency(cls, song: Song) -> None:
        df = get_bow_dataframe(song.words)
        freq = df['freq']
        words = df['word']
        for w, f in zip(words, freq):
            cls.upsert(w, song, f)

    @classmethod
    def upsert(cls, word: str, song: Song, frequency: float) -> 'WordOccurrenceInSong':
        try:
            # database note for sqlite:
            # https://docs.djangoproject.com/en/3.1/ref/databases/#sqlite-string-matching
            w = WordCache.objects.get(word__iexact=word)
        except WordCache.DoesNotExist:
            w = WordCache.objects.create(word=word)
        try:
            wo = cls.objects.get(word=w, appears_in=song)
            wo.frequency = frequency
            wo.save()
            return wo
        except WordOccurrenceInSong.DoesNotExist:
            return cls.objects.create(word=w, appears_in=song, frequency=frequency)
