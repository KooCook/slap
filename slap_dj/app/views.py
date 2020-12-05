# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from .models import Song, Artist
from .serializers import SongSerializer
from .support import LargeResultsSetPagination


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ('get', )


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows a song to be viewed.
    """
    queryset = Artist.objects.all()
