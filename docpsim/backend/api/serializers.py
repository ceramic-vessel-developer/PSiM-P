from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreate(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserReturn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
