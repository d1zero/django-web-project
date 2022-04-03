from django.urls import path, include
from rest_framework import routers
from .views import ToggleFavoriteArtistViewSet, ArtistViewSet

ArtistRouter = routers.SimpleRouter()
ArtistRouter.register('toggle-favorite', ToggleFavoriteArtistViewSet)
ArtistRouter.register('', ArtistViewSet)

urlpatterns = [
    path("artists/", include(ArtistRouter.urls))
]
