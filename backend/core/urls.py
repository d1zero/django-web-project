from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from albums.views import AlbumViewSet
from artists.views import ArtistViewSet

from genres.views import GenreViewSet
from playlists.views import PlaylistViewSet
from tracks.views import TrackViewSet

router = routers.SimpleRouter()
router.register('albums', AlbumViewSet)
router.register('artists', ArtistViewSet)
router.register('genres', GenreViewSet)
router.register('playlists', PlaylistViewSet)
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
