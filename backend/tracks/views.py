from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from authentication.models import UserFavorite
from .models import Track
from .serializers import TrackSerializer

class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except Track.DoesNotExist:
            raise NotFound(detail='Track was not found')


class ToggleFavoriteTrackViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavorite.objects.all()
    serializer_class = TrackSerializer
    model = Track

    def list(self, request):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)
        data = self.serializer_class(user_favs.tracks.all(), many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)

        try:
            self.serializer_class(user_favs.tracks.get(pk=pk)).data
            liked = True
        except self.model.DoesNotExist:
            liked = False

        return Response({'detail': liked})

    def create(self, request):
        user = request.user
        if 'trackId' not in request.data or len(request.data.get('trackId')) < 1:
            raise ParseError(detail='trackId must not be empty')

        pk = int(request.data.get('trackId'))
        user_favs = UserFavorite.objects.get(user=user)

        try:
            track = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail='track was not found')

        if track not in user_favs.Tracks.all():
            user_favs.Tracks.add(track)
        else:
            user_favs.tracks.remove(track)
        user_favs.save()
        return Response({'message':'success'})
