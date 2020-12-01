from typing import Union

from services.main import generate_song_to_model
from support.models import SongModel
from slap_dj.app.models import Song, Artist, Genre, SpotifyTrack
from django.core.exceptions import ObjectDoesNotExist


class SongSearcher:
    @classmethod
    def search_one(cls, title: str = None, **kwargs) -> Union[Song, None]:
        try:
            result = Song.objects.get(**kwargs)
            return result
        except ObjectDoesNotExist:
            fetched_result = cls.from_model(generate_song_to_model(title, kwargs['artists__name']))
            fetched_result.save()
            return fetched_result

    @classmethod
    def from_model(cls, song_model: SongModel) -> 'Song':
        inst = Song(title=song_model.name,
                    compressibility=song_model.compressibility,
                    lyrics=song_model.lyrics,
                    spotify_popularity=song_model.spotify_popularity)
        artists = []
        for artist_name in song_model.artist_names:
            try:
                artist = Artist.objects.filter(name=artist_name).get()
            except ObjectDoesNotExist:
                artist = Artist(name=artist_name)
                artist.save()
            artists.append(artist)
        songs = Song.objects.filter(title=song_model.name, artists__in=artists)
        if len(songs) > 0:
            return songs[0]
        inst.save()
        SpotifyTrack(song=inst, track_id=song_model.spotify_id,
                     album_id=song_model.spotify_album_id).save()
        for genre_label in song_model.genres:
            try:
                genre = Genre.objects.filter(name=genre_label).get()
            except ObjectDoesNotExist:
                genre = Genre(name=genre_label)
                genre.save()
            inst.genres.add(genre)
        for artist in artists:
            inst.artists.add(artist)
        return inst
