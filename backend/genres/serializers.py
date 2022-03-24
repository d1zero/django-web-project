from rest_framework import serializers
from authentication.models import UserFavorite
from .models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'