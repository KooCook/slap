from django.db import models

from repetition import get_bow_dataframe
from services.genius import tokenize_words
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
    def update_all_songs_word_frequency(cls, skip=True):
        for s in Song.objects.all():
            try:
                s = cls.objects.filter(appears_in=s)
                if skip and s is not None:
                    continue
            except cls.DoesNotExist:
                pass
            cls.update_song_word_frequency(s)

    @classmethod
    def update_song_word_frequency(cls, song: Song):
        tokenized = tokenize_words(song.lyrics)
        df = get_bow_dataframe(tokenized)
        freq = df['freq']
        words = df['word']
        for w, f in zip(words, freq):
            cls.upsert(w, song, f)

    @classmethod
    def upsert(cls, word: str, song: Song, frequency: float) -> 'WordOccurrenceInSong':
        try:
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
