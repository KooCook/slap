from django.db import models

from services.wikidata import get_artist_akas
from .base import Song


__all__ = ['Artist', 'ArtistAkas', 'ArtistInSong']


class Artist(models.Model):
    name = models.CharField(max_length=289)

    def as_dict(self) -> dict:
        return {'name': self.name}

    @classmethod
    def get(cls, name: str):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            inst = cls(name=name)
            inst.save()
            return inst

    def generate_akas(self):
        try:
            if len(ArtistAkas.objects.filter(artist=self)) >= 1:
                return
            for akas in get_artist_akas(self.name):
                ArtistAkas(artist=self, name=akas).save()
                print(f"generated for {self.name}: {akas}")
        except KeyError:
            print(f"skipped for {self.name}")

    @classmethod
    def generate_akas_all(cls):
        for o in cls.objects.all():
            o.generate_akas()


class ArtistAkas(models.Model):
    name = models.CharField(max_length=150, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class ArtistInSong(models.Model):

    class Role(models.TextChoices):
        Primary = "primary"
        Secondary = "secondary"
        Collaborator = "collaborator"
        Featured = "featured"

    class Meta:
        unique_together = ('artist', 'song')

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=Role.choices)

    @classmethod
    def upsert(cls, song: Song, artist: Artist):
        try:
            return cls.objects.get(song=song, artist=artist)
        except cls.DoesNotExist:
            inst = cls(song=song, artist=artist)
            inst.save()
            return inst
