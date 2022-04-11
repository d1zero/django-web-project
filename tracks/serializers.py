from rest_framework import serializers
from artists.serializers import ArtistSerializer
from genres.serializers import GenreSerializer
from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    artists_data = ArtistSerializer(source='artists', many=True)
    genres_data = GenreSerializer(source='genres', many=True)
    class Meta:
        model = Track
        exclude = ['artists', 'genres']
