from typing import Type

from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_swagger.views import get_swagger_view

from . import views
from .views import WordOccurrenceView, WordInLyricsCorrectnessView, WordRandomizationView, WordView, WordFrequencyView, \
    swagger_specs, SwaggerSpecsView
from .views.kpop import KPopGenreView
from .views.plot import RepetitionPopularityPlotView, RepetitionMatrixPlotView, SongWordFrequencyPlotView
from .views.word import WordsView, SongFromWordView

router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet, basename='Song')
router.register(r'genres', views.GenreViewSet)
router.register(r'artists', views.ArtistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/plot/rep-matrix/<song_id>', RepetitionMatrixPlotView.as_view()),
    path('api/plot/rep-pop', RepetitionPopularityPlotView.as_view()),
    path('api/words/song', SongFromWordView.as_view()),
    # TODO: query params: word <- 0 - 1 (0.9) Max
    # TODO: GET method: word, min_song_popularity, max_result=, shuffle = True, sect (orderby pop by default)
    # Returns: List[SongObject]
    path('api/words', WordsView.as_view()),
    # TODO: GET method: (params) min_relative_popularity, max_relative_popularity (required=False),
    # song_tags? (None = all), max_result=, shuffle = True (orderby pop by default)
    # maybe pagination NotImplemented
    # Returns: List[sanitized(WordObject), rel_pop?]
    path('api/songs/words/randomize', WordRandomizationView.as_view()),
    path('api/songs/<song_id>/words', WordView.as_view()),
    path('api/songs/<song_id>/word-frequency', WordFrequencyView.as_view()),
    path('api/songs/<song_id>/word-frequency/plot', SongWordFrequencyPlotView.as_view()),
    path('api/songs/kpop', KPopGenreView.as_view()),
    path('api/word-occur', WordOccurrenceView.as_view()),
    path('api/check/songs/word-in-lyrics', WordInLyricsCorrectnessView.as_view()),
    path('api/swagger-specs', SwaggerSpecsView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
