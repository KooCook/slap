from typing import List, Type, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from app_v2.models import Song
from app_v2.models.fields import CSVField
from app_v2.models.utils import upsert
from contract_models.song import SongModel
from services.wikidata import retrieve_songmodel_wikidata, retrieve_english_songs as populate_internal


def populate_wikidata_english_songs():
    song_list: List[SongModel] = populate_internal()
    for song in song_list:
        ws = upsert(WikidataSong, wikidata_id=song.wikidata_id)
        for artist in song.artists:
            p = upsert(WikidataArtist, name=artist)
            ws.performers.add(p)
        Song.objects.create(wikidata_song=ws)
        # TODO: call spotify next


class WikidataSong(models.Model):
    title = models.CharField(max_length=255)
    wikidata_id = models.CharField(max_length=13, unique=True,
                                   blank=False)
    performers = models.ManyToManyField('WikidataArtist', on_delete=models.SET_NULL, null=True)

    @classmethod
    def retrieve_song(cls, song_title: str, artists: List['Artist']) -> 'WikidataSong':
        if not artists:
            raise TypeError(f"NULL ARTIST!!!!! {artists}")
        s = retrieve_songmodel_wikidata(song_title=song_title,
                                        artists=list(map(lambda a: a.name, artists)))
        return upsert(cls, wikidata_id=s.wikidata_id)


class WikidataArtist(models.Model):
    name = models.CharField(max_length=255)
    alt_names = CSVField(item_type=str)
