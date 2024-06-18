from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Games, Teams, Checkpoints, Comments, Achievements


class UserCreate(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserReturn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AchievementReturn(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['id', 'description', 'bonus', 'treshold', 'checkpoint']


class CheckpointReturn(serializers.ModelSerializer):
    class Meta:
        model = Checkpoints
        fields = ['id', 'name', 'description', 'previous']


class CheckpointReturnAdmin(serializers.ModelSerializer):
    class Meta:
        model = Checkpoints
        fields = ['id', 'name', 'description', 'previous', 'qr_code_path']


class GameReturn(serializers.ModelSerializer):
    admin = UserReturn(source='game_admin')
    checkpoints = CheckpointReturn(many=True)
    achievements = AchievementReturn(many=True)

    class Meta:
        model = Games
        fields = ['id', 'name', 'description', 'max_team_size', 'admin', 'checkpoints', 'achievements']


class GameReturnStrip(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'name', 'description', 'max_team_size']


class GameCreate(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    description = serializers.CharField()
    max_team_size = serializers.IntegerField()
    game_admin_id = serializers.IntegerField()


class Comments(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class TeamReturn(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Teams
        fields = ['id', 'game', 'name', 'points', 'game_times', 'members']


class AchievementCreate(serializers.Serializer):
    description = serializers.CharField()
    bonus = serializers.IntegerField()
    treshold = serializers.IntegerField(allow_null=True, default=None)
    checkpoint_id = serializers.IntegerField(allow_null=True, default=None)


class CheckpointCreate(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    previous = serializers.IntegerField(allow_null=True, default=-1)
    qr_code_path = serializers.CharField(allow_null=True, default=None)


class TeamCreate(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    players = serializers.ListField(child=serializers.CharField())
