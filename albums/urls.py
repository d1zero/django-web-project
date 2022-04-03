from django.urls import path, include
from rest_framework import routers
from .views import ToggleFavoriteAlbumViewSet, AlbumViewSet

AlbumRouter = routers.SimpleRouter()
AlbumRouter.register('toggle-favorite', ToggleFavoriteAlbumViewSet)
AlbumRouter.register('', AlbumViewSet)

urlpatterns = [
    path("albums/", include(AlbumRouter.urls))
]
