from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
