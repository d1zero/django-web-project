from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
