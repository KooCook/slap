from django.urls import path, include
from rest_framework import routers

from . import views
from .views import WordOccurrenceView, WordInLyricsCorrectnessView, WordRandomizationView, WordView
from .views.kpop import KpopGenreView
from .views.plot import RepetitionPopularityPlotView, RepetitionMatrixPlotView, SongWordFrequencyPlotView

router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet, basename='Song')
router.register(r'genres', views.GenreViewSet)
# router.register(r'artist', views.ArtistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/plot/rep-matrix/<song_id>', RepetitionMatrixPlotView.as_view()),
    path('api/plot/rep-pop', RepetitionPopularityPlotView.as_view()),
    path('api/songs/words/randomize', WordRandomizationView.as_view()),
    path('api/songs/<song_id>/words', WordView.as_view()),
    path('api/songs/<song_id>/word-frequency/plot', SongWordFrequencyPlotView.as_view()),
    path('api/songs/kpop', KpopGenreView.as_view()),
    path('api/word-occur', WordOccurrenceView.as_view()),
    path('api/check/songs/word-in-lyrics', WordInLyricsCorrectnessView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
