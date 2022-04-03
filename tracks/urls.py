from django.urls import path, include
from rest_framework import routers
from .views import ToggleFavoriteTrackViewSet, TrackViewSet

TrackRouter = routers.SimpleRouter()
TrackRouter.register('toggle-favorite', ToggleFavoriteTrackViewSet)
TrackRouter.register('', TrackViewSet)

urlpatterns = [
    path("tracks/", include(TrackRouter.urls))
]
