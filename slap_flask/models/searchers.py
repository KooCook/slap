from typing import Union

from services.main import generate_song_to_model
from support.models import SongModel
from slap_dj.app.models import Song, Artist, Genre
from django.core.exceptions import ObjectDoesNotExist


class SongSearcher:
    @classmethod
    def search_one(cls, **kwargs) -> Union[Song, None]:
        try:
            result = Song.objects.get(**kwargs)
            return result
        except ObjectDoesNotExist:
            fetched_result = cls.from_model(generate_song_to_model(kwargs['title'], kwargs['artists__name']))
            fetched_result.save()
            return fetched_result

    @classmethod
    def from_model(cls, song_model: SongModel) -> 'Song':
        inst = Song(title=song_model.name,
                    compressibility=song_model.compressibility,
                    lyrics=song_model.lyrics)
        try:
            artist = Artist.objects.filter(name=song_model.artist_name).get()
        except ObjectDoesNotExist:
            artist = Artist(name=song_model.artist_name)
            artist.save()
        inst.save()
        for genre_label in song_model.genres:
            try:
                genre = Genre.objects.filter(name=genre_label).get()
            except ObjectDoesNotExist:
                genre = Genre(name=genre_label)
                genre.save()
            inst.genres.add(genre)
        inst.artists.add(artist)
        return inst
