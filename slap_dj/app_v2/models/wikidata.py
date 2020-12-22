from typing import List
import json

from django.db import models

from app_v2.models.youtube import YoutubeVideo
from app_v2.models.base import Song, Artist, ArtistSong
from app_v2.models.spotify import retrieve_from_song_title_and_possible_artists
from app_v2.db.utils import upsert
from contract_models.song import SongModel
from services.wikidata import retrieve_songmodel_wikidata, retrieve_english_songs as populate_internal, \
    retrieve_song_model_from_wikidata_id

__all__ = [
    'populate_wikidata_english_songs',
    'WikidataSong',
    'WikidataArtist',
]


def populate_wikidata_english_songs():
    song_list: List[SongModel] = populate_internal()
    for song in song_list:
        ws = upsert(WikidataSong, title=song.name.strip(), wikidata_id=song.wikidata_id)
        artists: List[Artist] = []
        assert song.artists, song.artists
        for artist in song.artists:
            p = upsert(WikidataArtist, name=artist.name.strip())
            ws.performers.add(p)
            a = upsert(Artist, wikidata_artist=p)
            artists.append(a)
        assert artists, artists

        spotify_songs = retrieve_from_song_title_and_possible_artists(song.name.strip(), song.artist_names)
        for spotify_song in spotify_songs:
            # TODO: Fix error: duplicate spotify song
            s = upsert(Song, wikidata_song=ws, spotify_song=spotify_song)
            break
        else:
            # BAD: no spotify songs for the wikidata entry
            s = upsert(Song, wikidata_song=ws)
        for at in artists:
            upsert(ArtistSong, artist=at, song=s)
        # break
        s.link_to_genius()
        s.update_compression_ratio()


class WikidataGenre(models.Model):
    wikidata_id = models.CharField(max_length=13, unique=True)
    label = models.CharField(max_length=255)


class WikidataSong(models.Model):
    title = models.CharField(max_length=255)
    wikidata_id = models.CharField(max_length=13, unique=True,
                                   blank=False)
    performers = models.ManyToManyField('WikidataArtist')
    genres = models.ManyToManyField('WikidataGenre')

    @classmethod
    def retrieve_song(cls, song_title: str, artists_names: List[str]) -> 'WikidataSong':
        # Ensure that it at least has an ID
        if not artists_names:
            raise TypeError(f"NULL ARTIST!!!!! {artists_names}")
        s = retrieve_songmodel_wikidata(song_title=song_title,
                                        artists=artists_names)
        return upsert(cls, title=s.name, wikidata_id=s.wikidata_id)

    @classmethod
    def retrieve_all_info_from_id(cls):
        for inst in cls.objects.all():
            if inst.wikidata_id:
                inst.retrieve_info_from_id()

    def retrieve_info_from_id(self):
        # Retrieve youtube ids from wikidata service
        try:
            s = retrieve_song_model_from_wikidata_id(wikidata_id=self.wikidata_id)
        except KeyError:
            print(self, self.wikidata_id)
            raise

        if s.name.upper() == self.wikidata_id.upper():
            pass
        else:
            self.title = s.name

        assert len(s.genres) == len(s.genre_ids)
        for genre, genre_id in zip(s.genres, s.genres):
            g = upsert(WikidataGenre, wikidata_id=genre_id, label=genre)
            self.genres.add(g)

        for yt_id in s.youtube_ids:
            yt = upsert(YoutubeVideo, video_id=yt_id)
            self.song.youtube_videos.add(yt)
        self.save()


class WikidataArtist(models.Model):
    name = models.CharField(max_length=255)
    alt_names_serialized = models.CharField(max_length=1000)

    @property
    def alt_names(self) -> List[str]:
        return json.loads(self.alt_names_serialized)

    @alt_names.setter
    def alt_names(self, value):
        self.alt_names_serialized = json.dumps(value)
