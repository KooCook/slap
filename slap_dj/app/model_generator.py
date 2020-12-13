from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from app.services.main import generate_song_to_model
from .models import Song, Artist, SpotifyTrack, Genre, ArtistInSong
from app.support.models import SongModel


def retrieve_cached_song(title: str = None, pk: str = None, **kwargs) -> Union[Song, None]:
    try:
        if pk:
            result = Song.objects.get(pk=pk)
        else:
            result = Song.objects.filter(title=title, **kwargs)[0]
        return result
    except (ObjectDoesNotExist, IndexError):
        fetched_result = insert_song_from_model(generate_song_to_model(title, kwargs['artists__name']))
        fetched_result.save()
        return fetched_result


def insert_song_from_model(song_model: SongModel) -> 'Song':
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
    for idx, artist in enumerate(artists):
        ArtistInSong(artist=artist, song=inst, role='primary' if idx == 0 else 'secondary').save()
    return inst
