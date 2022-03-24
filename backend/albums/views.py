from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
