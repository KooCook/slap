from app.init import start_django_lite

start_django_lite()

from app_v2.models import populate_wikidata_english_songs

from app.management.commands._populate_models import generate_english_songs
from app.models import YouTubeVideo, WordCache, ArtistInSong, WordOccurrenceInSong, Song

# import spacy
# spacy.load("en_core_web_sm")

if __name__ == '__main__':
    populate_wikidata_english_songs()
    # for w in WordOccurrenceInSong.objects.filter(appears_in=s):
    #     w.word.update_popularity()
    #     print(w.word.popularity_score)
    # w: WordCache = WordCache.objects.get(word='I')
    # print(w.popularity)
    # ArtistInSong.objects.get(pk=708).delete()
    # for word in WordCache.objects.all():
    #     word.update_popularity()
   #  YouTubeVideo.update_all_video_stats()
    # generate_english_songs()
    #WordOccurrenceInSong.update_all_songs_word_frequency()
