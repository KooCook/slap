from django.urls import path, include
from rest_framework import routers

from . import views
from .views import WordOccurrenceView

router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'genres', views.GenreViewSet)
# router.register(r'artist', views.ArtistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/word-occur', WordOccurrenceView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
