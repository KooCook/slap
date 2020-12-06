from slap_dj.app.init import start_django_lite

start_django_lite()

from slap_dj.app.models.word import WordOccurrenceInSong

if __name__ == '__main__':
    WordOccurrenceInSong.update_all_songs_word_frequency()
