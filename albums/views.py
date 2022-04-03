from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from authentication.models import UserFavorite
from .models import Album
from .serializers import AlbumSerializer

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except Album.DoesNotExist:
            raise NotFound(detail='Album was not found')



class ToggleFavoriteAlbumViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavorite.objects.all()
    serializer_class = AlbumSerializer
    model = Album

    def list(self, request):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)
        data = self.serializer_class(user_favs.albums.all(), many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)

        try:
            self.serializer_class(user_favs.albums.get(pk=pk)).data
            liked = True
        except self.model.DoesNotExist:
            liked = False

        return Response({'detail': liked})

    def create(self, request):
        user = request.user
        if 'albumId' not in request.data or len(request.data.get('albumId')) < 1:
            raise ParseError(detail='albumId must not be empty')

        pk = int(request.data.get('albumId'))
        user_favs = UserFavorite.objects.get(user=user)

        try:
            album = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail='Album was not found')

        if Album not in user_favs.albums.all():
            user_favs.albums.add(album)
        else:
            user_favs.albums.remove(album)
        user_favs.save()
        return Response({'message':'success'})
