from django.db import models
from django.db.models.aggregates import Min, Max
from scipy import special

from app.support.repetition import get_bow_dataframe
from .base import Song


__all__ = ['WordCache', 'WordOccurrenceInSong']


class WordCache(models.Model):
    word = models.CharField(max_length=289, unique=True)
    occurs_in_song = models.ManyToManyField(Song, through='WordOccurrenceInSong')
    popularity_score = models.FloatField(null=True)

    # wordoccurrenceinsong_set from ManyToManyField
    @classmethod
    def min_relative_popularity(cls) -> float:
        return WordCache.objects.aggregate(Min('popularity_score'))['popularity_score__min']

    # compared to max
    @classmethod
    def max_popularity(cls) -> float:
        s = WordCache.objects.aggregate(Max('popularity_score'))
        return s['popularity_score__max']

    @property
    def relative_popularity(self) -> float:
        if not self.popularity_score:
            return 0
        return self.popularity_score / self.max_popularity()

    def update_popularity(self):
        word_occurrence_in_songs = self.wordoccurrenceinsong_set.all()
        lst = []
        for wois in word_occurrence_in_songs:
            try:
                lst.append(wois.weighted_frequency * wois.appears_in.weighted_popularity)
            except (models.base.ObjectDoesNotExist, ValueError):
                pass
        self.popularity_score = sum(lst)
        self.save()

    # @property
    # def popularity(self) -> float:
    #     word_occurrence_in_songs = self.wordoccurrenceinsong_set.all()
    #     lst = []
    #     skip_count = 0
    #     for wois in word_occurrence_in_songs:
    #         try:
    #             lst.append(wois.weighted_frequency * wois.appears_in.weighted_popularity)
    #         except models.base.ObjectDoesNotExist:
    #             skip_count += 1
    #     # print(skip_count)
    #     # print(len(lst))
    #     return sum(lst)


class WordOccurrenceInSong(models.Model):
    word = models.ForeignKey(WordCache, on_delete=models.CASCADE)
    appears_in = models.ForeignKey(Song, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    @property
    def weighted_frequency(self) -> float:
        """ Returns a number between 0 and 1 """
        w = float(special.expit(self.frequency - 2.8))
        assert 0 <= w <= 1, f"weighted_frequency of {self} not in bound: {w}"
        return w

    @classmethod
    def update_all_songs_word_frequency(cls, skip: bool = True) -> None:
        for song in Song.objects.all():
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
