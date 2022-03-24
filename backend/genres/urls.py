from django.urls import path, include
from rest_framework import routers
from .views import ToggleFavoriteGenreViewSet, GenreViewSet

GenreRouter = routers.SimpleRouter()
GenreRouter.register('toggle-favorite', ToggleFavoriteGenreViewSet)
GenreRouter.register('', GenreViewSet)

urlpatterns = [
    path("genres/", include(GenreRouter.urls))
]
