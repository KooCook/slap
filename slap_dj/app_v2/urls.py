from django.urls import path, include
from rest_framework import routers

from app_v2.views.base import WordOccurrenceView, WordInLyricsCorrectnessView, WordRandomizationView, WordView, WordFrequencyView, SwaggerSpecsView, SongViewSet, GenreViewSet, ArtistViewSet
from app_v2.views.kpop import KPopGenreView
from app_v2.views.plot import RepetitionPopularityPlotView, RepetitionMatrixPlotView, SongWordFrequencyPlotView
from app_v2.views.word import WordsView, SongFromWordView

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet, basename='Song')
router.register(r'genres', GenreViewSet)
router.register(r'artists', ArtistViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/plot/rep-matrix/<song_id>', RepetitionMatrixPlotView.as_view()),
    path('api/plot/rep-pop', RepetitionPopularityPlotView.as_view()),
    path('api/words/song', SongFromWordView.as_view()),
    path('api/words', WordsView.as_view()),
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
