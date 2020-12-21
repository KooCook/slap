from typing import Iterable, List

from django.db import models

from app.support.repetition import get_words
from app_v2.db.utils import upsert
from contract_models.genius import GeniusSongModel
from services.genius import remove_sections, tokenize_words


class GeniusSong(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField()
    song_id = models.CharField(max_length=15, unique=True,
                               blank=False)

    @property
    def words(self) -> List[str]:
        return list(get_words(remove_sections(self.lyrics)))

    @property
    def word_count(self) -> int:
        return len(tokenize_words(self.lyrics))

    @classmethod
    def retrieve_song(cls, title: str, artists_names: List['Artist']) -> 'GeniusSong':
        # Ensure that it at least has an ID
        s = GeniusSongModel.from_title_and_artist(title, artists_names[0])
        return upsert(cls,
                      title=s.title,
                      lyrics=s.lyrics,
                      song_id=s.genius_id)


class GeniusArtist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=15, unique=True,
                                 blank=False)
