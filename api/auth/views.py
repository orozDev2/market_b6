from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from account.models import User
from api.auth.serializers import LoginSerializer, ReadUserSerializer, RegisterSerializer


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if not user:
            return Response({'detail': 'The user does not exist or incorrect password.'}, status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        user_serializer = ReadUserSerializer(user, context={'request': request})

        data = {
            **user_serializer.data,
            'token': token.key
        }

        return Response(data)




class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        user_serializer = ReadUserSerializer(user, context={'request': request})

        data = {
            **user_serializer.data,
            'token': token.key
        }

        return Response(data)
