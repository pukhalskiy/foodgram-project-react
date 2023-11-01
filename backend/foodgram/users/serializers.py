from rest_framework import serializers
from rest_framework import status

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)