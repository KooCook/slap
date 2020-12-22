from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from app_v2.models import Word, WordSong, Song
from app.serializers import WordOccurrenceSerializer, WordSerializer, SongWithWordSerializer, SongShortSerializer


class WordsView(APIView):
    # GET method: (params) min_relative_popularity, max_relative_popularity (required=False),
    # song_tags? (None = all), max_result=, shuffle = True (orderby pop by default)
    # maybe pagination NotImplemented
    # Returns: List[sanitized(WordObject), rel_pop?]
    def get(self, request: Request):
        min_rel_pop = float(self.request.query_params.get('min_relative_popularity', 0))
        max_rel_pop = float(self.request.query_params.get('max_relative_popularity', 0.8))
        song_tag = self.request.query_params.get('song_tag', None)
        max_result: int = self.request.query_params.get('max_result', 50)
        shuffle: bool = self.request.query_params.get('shuffle', False)
        if song_tag:
            queryset = Word.objects.filter(wordsong__song__spotify_song__genres__name=song_tag)
        else:
            queryset = Word.objects.all()
        if shuffle:
            queryset = queryset.order_by('?')
        wc = [w for w in queryset if min_rel_pop <= w.relative_popularity <= max_rel_pop][:max_result]
        s = WordSerializer(wc, many=True)
        return Response(s.data)


class SongFromWordView(APIView):
    """
    Example Song by CW
    """
    def get(self, request: Request):
        word = self.request.query_params.get('word', '')
        # TODO: song section
        section = self.request.query_params.get('section', '')
        min_pop = float(self.request.query_params.get('min_song_popularity', 0.5))
        max_result: int = int(self.request.query_params.get('max_result', 50))
        shuffle: bool = self.request.query_params.get('shuffle', False)
        queryset = Song.objects.filter(wordoccurrenceinsong__word__word__iexact=word)
        if shuffle:
            queryset = queryset.order_by('?')
        result = []
        for s in queryset:
            try:
                if min_pop <= s.weighted_popularity:
                    result.append(s)
            except ValueError:
                pass
        wc = result[:max_result]
        s = SongShortSerializer(wc, many=True)
        return Response(s.data)
