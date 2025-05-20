from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import ConfirmUser

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)


class UserAuthSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exist!')