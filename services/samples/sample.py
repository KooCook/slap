from slap_dj.app.init import start_django_lite

start_django_lite()

from repetition import get_bow_dataframe, get_words
from slap_dj.app.models import Song

song = Song.objects.get(pk=85)
print(list(get_bow_dataframe(get_words(song.lyrics))['word']))
