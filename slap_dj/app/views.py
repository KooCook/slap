from nltk.stem import PorterStemmer

ps = PorterStemmer()
# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import PaginatedViewMixin
from .models import Song, Artist, Genre
from .models.word import WordCache
from .serializers import SongSerializer, GenreSerializer, WordOccurrenceSerializer
from .support import LargeResultsSetPagination


class SongViewSet(viewsets.ModelViewSet):
    """
    An API endpoint that allows songs to be viewed.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ('get', )


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


class WordOccurrenceView(APIView, PaginatedViewMixin):
    """A view that returns the occurrences of words in songs in JSON.
    """
    pagination_class = LargeResultsSetPagination
    serializer_class = WordOccurrenceSerializer
    http_method_names = ('get', )

    def get(self, request, format=None, *args, **kwargs):
        word = self.request.query_params.get('word', '')
        occurrences = WordCache.objects.filter(word__icontains=word)
        occurrences = list(filter(lambda x: ps.stem(x.word) in word, occurrences))
        page = self.paginate_queryset(occurrences)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(occurrences, many=True)
        return Response(serializer.data)
