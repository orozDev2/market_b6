from rest_framework import serializers

from account.models import User


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'groups',
            'date_joined',
            'user_permissions',
            'password',
            'is_staff',
            'is_superuser',
            'is_active',
        )