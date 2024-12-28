from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.auth.serializers import LoginSerializer, ReadUserSerializer


@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
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
