from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from authentication.models import UserFavorite
from .models import Genre
from .serializers import GenreSerializer


class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except Genre.DoesNotExist:
            raise NotFound({'message': 'Genre was not found'})


class ToggleFavoriteGenreViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavorite.objects.all()
    serializer_class = GenreSerializer
    model = Genre

    def list(self, request):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)
        data = self.serializer_class(user_favs.genres.all(), many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        user_favs = UserFavorite.objects.get(user=user)

        try:
            self.serializer_class(user_favs.genres.get(pk=pk)).data
            liked = True
        except self.model.DoesNotExist:
            liked = False

        return Response({'message': liked})

    def create(self, request):
        user = request.user
        if 'genreId' not in request.data or \
                len(request.data.get('genreId')) < 1:
            raise ParseError({'message': 'genreId must not be empty'})

        pk = int(request.data.get('genreId'))
        user_favs = UserFavorite.objects.get(user=user)

        try:
            genre = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound({'message': 'Genre was not found'})

        if genre not in user_favs.genres.all():
            user_favs.genres.add(genre)
        else:
            user_favs.genres.remove(genre)
        user_favs.save()
        return Response({'message': 'success'})
