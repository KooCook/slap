from typing import List

from app.model_generator import retrieve_cached_song, insert_song_from_model
from app.models import Artist, YouTubeVideo, Song, ArtistInSong
from services.wikidata import get_kpop_songs, retrieve_english_songs


def generate_artists():
    Artist.generate_akas_all()


def chain_kpop_songs(limit: int = 1000):
    records: List = get_kpop_songs().to_dict('records')
    for record in records[:limit]:
        title = record['song_title']
        try:
            first = record['performers'].split(",")[0]
            s = retrieve_cached_song(title=title, artists__name=first)
            ArtistInSong.upsert(song=s, artist=Artist.get(first))
            vid = record['video_id']
            YouTubeVideo.upsert_video(vid, s)
            print(f"done {title} - {record['performers']}")
        except (NameError, TypeError, AttributeError):
            print(f"Service retrieval error {title} - {record['performers']}")


def generate_english_songs(limit: int = 1000):
    songs = retrieve_english_songs()
    for song in songs:
        song.update_field_data()
        insert_song_from_model(song)
        print(f"{song.name} - {song.artist_names}")
