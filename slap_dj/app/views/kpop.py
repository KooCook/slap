import pandas
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Song

from repetition import get_bow_dataframe


def check_word_english_alpha(word: str) -> bool:
    """
    Checks whether the word is an English word or not

    Args:
        word: Any given word

    Returns:
        Whether the word is an English word or not

    Examples:
        >>> check_word_english_alpha("English")
        True
        >>> check_word_english_alpha("영원한")
        False
    """
    return word.upper() != word.lower()


class KpopGenreView(APIView):
    def get(self, request):
        kpop_songs = Song.objects.filter(genres__name='k-pop')
        df: pandas.DataFrame = kpop_songs.to_dataframe()
        ratios = []
        eng_words_each = []
        for idx, song in enumerate(kpop_songs):
            tokenized = song.words
            eng_words = list(filter(check_word_english_alpha, tokenized))
            ratios.append(len(eng_words) / len(tokenized))
            eng_words_each.append(get_bow_dataframe(eng_words))
        df['english_ratio'] = ratios
        df['eng_words'] = eng_words_each

        return Response(df)
