from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from genres.views import ToggleFavoriteGenreViewSet, GenreViewSet
from albums.views import ToggleFavoriteAlbumViewSet, AlbumViewSet
from artists.views import ToggleFavoriteArtistViewSet, ArtistViewSet
from playlists.views import ToggleFavoritePlaylistViewSet, PlaylistViewSet
from tracks.views import ToggleFavoriteTrackViewSet, TrackViewSet


router = routers.SimpleRouter()
router.register('albums/toggle-favorite', ToggleFavoriteAlbumViewSet)
router.register('albums', AlbumViewSet)
router.register('artists/toggle-favorite', ToggleFavoriteArtistViewSet)
router.register('artists', ArtistViewSet)
router.register('genres/toggle-favorite', ToggleFavoriteGenreViewSet)
router.register('genres', GenreViewSet)
router.register('playlists/toggle-favorite', ToggleFavoritePlaylistViewSet)
router.register('playlists', PlaylistViewSet)
router.register('tracks/toggle-favorite', ToggleFavoriteTrackViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
