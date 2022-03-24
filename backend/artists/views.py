from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from authentication.models import UserFavorite
from .models import Artist
from .serializers import ArtistSerializer

class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except Artist.DoesNotExist:
            raise NotFound(detail='Artist was not found')



class ToggleFavoriteArtistViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavorite.objects.all()
    serializer_class = ArtistSerializer
    model = Artist

    def list(self, request):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)
        data = self.serializer_class(user_favs.artists.all(), many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)

        try:
            self.serializer_class(user_favs.artists.get(pk=pk)).data
            liked = True
        except self.model.DoesNotExist:
            liked = False

        return Response({'detail': liked})

    def create(self, request):
        user = request.user
        if 'artistId' not in request.data or len(request.data.get('artistId')) < 1:
            raise ParseError(detail='artistId must not be empty')

        pk = int(request.data.get('artistId'))
        user_favs = UserFavorite.objects.get(user=user)

        try:
            artist = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail='Artist was not found')

        if artist not in user_favs.artists.all():
            user_favs.artists.add(artist)
        else:
            user_favs.artists.remove(artist)
        user_favs.save()
        return Response({'message':'success'})
