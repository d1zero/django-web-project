from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from authentication.views import UserViewSet
from genres.views import ToggleFavoriteGenreViewSet, GenreViewSet
from albums.views import ToggleFavoriteAlbumViewSet, AlbumViewSet, GetLatestTwoYearsAlbumsAPIView
from artists.views import ToggleFavoriteArtistViewSet, ArtistViewSet
from playlists.views import ToggleFavoritePlaylistViewSet, PlaylistViewSet
from tracks.views import ToggleFavoriteTrackViewSet, TrackViewSet
from .views import schema_view


router = routers.SimpleRouter()
router.register('auth', UserViewSet)
router.register('albums/toggle-favorite', ToggleFavoriteAlbumViewSet, basename='albums-userfavorite')
router.register('albums', AlbumViewSet)
router.register('artists/toggle-favorite', ToggleFavoriteArtistViewSet, basename='artists-userfavorite')
router.register('artists', ArtistViewSet)
router.register('genres/toggle-favorite', ToggleFavoriteGenreViewSet, basename='genres-userfavorite')
router.register('genres', GenreViewSet)
router.register('playlists/toggle-favorite', ToggleFavoritePlaylistViewSet, basename='playlists-userfavorite')
router.register('playlists', PlaylistViewSet)
router.register('tracks/toggle-favorite', ToggleFavoriteTrackViewSet, basename='tracks-userfavorite')
router.register('tracks', TrackViewSet)

# from django.http import HttpResponse
# def trigger_error(request):
#     division_by_zero = 0 / 1
#     return HttpResponse('asdsad')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/albums/latest/', GetLatestTwoYearsAlbumsAPIView.as_view()),
    path('api/', include(router.urls)),
    # path('sentry-debug/', trigger_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'),
    ]
