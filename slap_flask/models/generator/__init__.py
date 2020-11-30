from slap_flask.models.song import Song
from services.spotify import search_for_song
from services.genius import search_for_song_lyrics, clean_lyrics
from repetition import calculate_repetition

song_tuples = (("Needed Me", "Rihanna"),)


def generate_song_to_db(song_name, song_artist):
    s = search_for_song(song_name, song_artist)
    lyrics = search_for_song_lyrics(song_name, song_artist)
    cmp = calculate_repetition(clean_lyrics(lyrics))
    Song(name=s.name, artist=s.artist_name, lyrics=lyrics, compressibility=cmp).save()


def start_generating():
    for s in song_tuples:
        generate_song_to_db(s[0], s[1])
