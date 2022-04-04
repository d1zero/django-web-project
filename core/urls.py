from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from authentication.views import UserViewSet
from genres.views import ToggleFavoriteGenreViewSet, GenreViewSet
from albums.views import ToggleFavoriteAlbumViewSet, AlbumViewSet
from artists.views import ToggleFavoriteArtistViewSet, ArtistViewSet
from playlists.views import ToggleFavoritePlaylistViewSet, PlaylistViewSet
from tracks.views import ToggleFavoriteTrackViewSet, TrackViewSet
from .views import schema_view


router = routers.SimpleRouter()
router.register('auth', UserViewSet)
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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
