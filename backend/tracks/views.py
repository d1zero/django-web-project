from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
