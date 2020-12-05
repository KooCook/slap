from django.db import models

from slap_dj.app.models import Song


class WordCache(models.Model):
    word = models.CharField(max_length=289)
    frequency = models.IntegerField()


class WordOccurrenceInSong(models.Model):
    word = models.ForeignKey(WordCache, on_delete=models.CASCADE)
    appears_in = models.ForeignKey(Song, on_delete=models.CASCADE)
