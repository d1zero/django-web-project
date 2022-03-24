from django.urls import path, include
from rest_framework import routers
from .views import ToggleFavoritePlaylistViewSet, PlaylistViewSet

PlaylistRouter = routers.SimpleRouter()
PlaylistRouter.register('toggle-favorite', ToggleFavoritePlaylistViewSet)
PlaylistRouter.register('', PlaylistViewSet)

urlpatterns = [
    path("playlists/", include(PlaylistRouter.urls))
]
