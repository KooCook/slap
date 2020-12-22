import pandas
from rest_framework.response import Response
from rest_framework.views import APIView

from app_v2.models import Song

from app.support.repetition import get_bow_dataframe
from utils.nlp import extract_eng_words


class KPopGenreView(APIView):
    def get(self, request):
        kpop_songs = Song.objects.filter(spotify_song__genres__name='k-pop')
        df: pandas.DataFrame = kpop_songs.to_dataframe()
        ratios = []
        eng_words_each = []
        for idx, song in enumerate(kpop_songs):
            eng_words = extract_eng_words(song.words)
            ratios.append(len(eng_words) / len(song.words))
            eng_words_each.append(get_bow_dataframe(eng_words))
        df['english_ratio'] = ratios
        df['eng_words'] = eng_words_each
        return Response(df)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
