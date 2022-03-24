from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from albums.urls import AlbumRouter
from artists.urls import ArtistRouter
from genres.urls import GenreRouter
from playlists.urls import PlaylistRouter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('albums.urls')),
    path('api/', include('artists.urls')),
    path('api/', include('genres.urls')),
    path('api/', include('playlists.urls')),
    path('api/', include('tracks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
