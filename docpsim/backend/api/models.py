from django.db import models
from django.contrib.auth.models import User


class Games(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    max_team_size = models.IntegerField()
    game_admmin = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'games'


class Teams(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    points = models.IntegerField()
    game_times = models.JSONField(default=list)

    class Meta:
        db_table = 'team'


class TeamMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_members'


class Checkpoints(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    qr_code_path = models.CharField(max_length=256)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    previous = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'checkpoints'


class Unlocked(models.Model):
    checkpoint = models.ForeignKey(Checkpoints, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

    class Meta:
        db_table = 'unlocked'


class Comments(models.Model):
    comment = models.TextField()
    date_time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    checkpoint = models.ForeignKey(Checkpoints, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'


class Achievements(models.Model):
    description = models.TextField()
    unlocked = models.BooleanField(default=False)
    bonus = models.IntegerField()
    treshold = models.IntegerField(null=True, blank=True)
    checkpoint = models.ForeignKey(Checkpoints, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

    class Meta:
        db_table = 'achivements'
