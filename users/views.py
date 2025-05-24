from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializer import UserCreateSerializer, UserAuthSerializer, ConfirmSerializer
from .models import ConfirmUser
import random

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username, password=password)
        user.is_active = False
        user.save()

        code = str(random.randint(100000, 999999))
        ConfirmUser.objects.create(user=user, code=code)

        return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id, 'confirm_code': code})


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(username=username)
            confirmation = ConfirmUser.objects.get(user=user)

            if confirmation.code == code:
                user.is_active = True
                user.save()
                confirmation.delete()
                return Response({'detail': "Пользователь подтвержден!"})
            else:
                return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ConfirmUser.DoesNotExist):
            return Response({'error': 'Пользователь или код не найден'}, status=status.HTTP_404_NOT_FOUND)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(status=status.HTTP_401_UNAUTHORIZED)
