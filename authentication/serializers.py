from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'date_joined',
                  'avatar']
        extra_kwargs = {
            'email': {'error_messages': {'required': 'Email must not be empty',
                                         'blank': 'Email must not be empty'}},
            'username': {'error_messages': {'required': 'Username must not\
                            be empty', 'blank': 'Username must not be empty'}},
            'password': {'write_only': True, 'error_messages':
                         {'required': 'Password must not be empty',
                          'blank': 'Password must not be empty'}}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
