from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from authentication.models import UserFavorite
from .models import Playlist
from .serializers import PlaylistSerializer

class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except Playlist.DoesNotExist:
            raise NotFound(detail='Playlist was not found')


class ToggleFavoritePlaylistViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavorite.objects.all()
    serializer_class = PlaylistSerializer
    model = Playlist

    def list(self, request):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)
        data = self.serializer_class(user_favs.playlists.all(), many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)

        try:
            self.serializer_class(user_favs.playlists.get(pk=pk)).data
            liked = True
        except self.model.DoesNotExist:
            liked = False

        return Response({'detail': liked})

    def create(self, request):
        user = request.user
        if 'playlistId' not in request.data or len(request.data.get('playlistId')) < 1:
            raise ParseError(detail='playlistId must not be empty')

        pk = int(request.data.get('playlistId'))
        user_favs = UserFavorite.objects.get(user=user)

        try:
            playlist = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail='Playlist was not found')

        if playlist not in user_favs.playlists.all():
            user_favs.playlists.add(playlist)
        else:
            user_favs.playlists.remove(playlist)
        user_favs.save()
        return Response({'message':'success'})