import random
from typing import List

from django.db.models import Max
from rest_framework import schemas, filters
from rest_framework.schemas.openapi import AutoSchema

from services.genius import tokenize_words
from support.init.nltk import initialize_nltk
from ..model_generator import SongGen

initialize_nltk()
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from rest_framework import viewsets
from rest_framework.compat import coreapi
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import ManualSchema, openapi as openapi_schema

from ..mixins import PaginatedViewMixin
from ..models import Song, Artist, Genre
from ..models.word import WordCache
from ..serializers import SongSerializer, GenreSerializer, WordOccurrenceSerializer
from ..support import LargeResultsSetPagination

ps = SnowballStemmer('english')


class SongViewSetParams(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        title = request.query_params.get('title', None)
        if title is not None:
            results = queryset.filter(title__istartswith=title)
        else:
            results = queryset.all()
        return results

    def get_schema_operation_parameters(self, view):
        return [{
            'name': 'title',
            'required': False,
            'in': 'query',
            'description': 'The partial title of this song',
            'schema': {
                'type': 'string'
            }
        }]


class SongViewSet(viewsets.ModelViewSet):
    """
    An API endpoint that allows songs to be viewed.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ('get', )
    filter_backends = [SongViewSetParams]


class ArtistViewSet(viewsets.ModelViewSet):
    """
    An API endpoint that allows artists to be viewed.
    """
    queryset = Artist.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ('get',)


def get_cached_word_occurrences(word: str, song_title: str = None,
                                artist_name: str = None, **kwargs) -> List[WordCache]:
    if song_title:
        kwargs['occurs_in_song__title__icontains'] = song_title
    if artist_name:
        kwargs['occurs_in_song__artists__name__iexact'] = artist_name
    occurrences = WordCache.objects.filter(word__icontains=word, **kwargs)
    return list(filter(lambda x: ps.stem(x.word.lower()) in word.lower(), occurrences))


class WordOccurrenceView(APIView, PaginatedViewMixin):
    """A view that returns the occurrences of words in songs in JSON.
    """
    pagination_class = LargeResultsSetPagination
    serializer_class = WordOccurrenceSerializer

    def get(self, request, *args, **kwargs):
        word = request.query_params.get('word', '')
        occurrences = get_cached_word_occurrences(word)
        page = self.paginate_queryset(occurrences)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(occurrences, many=True)
        return Response(serializer.data)


class WordInLyricsCorrectnessView(APIView):
    def get(self, *args, **kwargs):
        word = self.request.query_params.get('word', '')
        title = self.request.query_params.get('title', None)
        artist = self.request.query_params.get('artist', None)
        if title and artist:
            occurrences = get_cached_word_occurrences(word, title, artist)
            result = len(occurrences) > 0
            return Response({'correct': result})
        else:
            return Response({'result': 'Must provide song title and artist name'}, 400)


class WordRandomizationView(APIView):
    def get(self, *args, **kwargs):
        no_stopwords = True
        max_id = WordCache.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            word: WordCache = WordCache.objects.filter(pk=pk).first()
            if word:
                if word.word in stopwords.words('english') and no_stopwords:
                    continue
                return Response({'word': word.word})


class WordView(APIView):
    """
    A list of words in the given song lyrics
    """
    def get(self, request, song_id: str):
        s = SongGen.search_one(pk=song_id)
        return Response({'words': tokenize_words(s.lyrics)})
