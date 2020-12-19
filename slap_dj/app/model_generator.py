from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from services.main import generate_song_to_model
from .models import Song, Artist, SpotifyTrack, Genre, ArtistInSong, YouTubeVideo
from contract_models.song import SongModel


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


def check_song_existence(title: str, artist_name: str) -> bool:
    if Song.objects.filter(title=title, artists__name=artist_name):
        return True
    return False


def insert_song_from_model(song_model: SongModel) -> 'Song':
    inst = Song(title=song_model.name,
                compressibility=song_model.compressibility,
                lyrics=song_model.lyrics,
                spotify_popularity=song_model.spotify_popularity,
                wikidata_id=song_model.wikidata_id,
                genius_id=song_model.genius_id)
    artists = []
    for artist in song_model.artists:
        try:
            artist = Artist.objects.get(name=artist.name)
        except ObjectDoesNotExist:
            artist = Artist(name=artist.name)
            artist.save()
        artists.append(artist)
    songs = Song.objects.filter(title=song_model.name, artists__in=artists)
    if len(songs) > 0:
        return songs[0]
    inst.save()
    SpotifyTrack.upsert(song=inst, track_id=song_model.spotify_id,
                        album_id=song_model.spotify_album_id).save()
    for youtube_id in song_model.youtube_ids:
        if youtube_id:
            YouTubeVideo.upsert_video(song=inst, video_id=youtube_id.strip())
    for genre_label in song_model.genres:
        try:
            genre = Genre.objects.get(name=genre_label)
        except ObjectDoesNotExist:
            genre = Genre(name=genre_label)
            genre.save()
        inst.genres.add(genre)
    for idx, artist in enumerate(artists):
        ArtistInSong(artist=artist, song=inst, role=ArtistInSong.Role.Primary.value if idx == 0 else ArtistInSong.Role.Secondary.value).save()
    return inst
