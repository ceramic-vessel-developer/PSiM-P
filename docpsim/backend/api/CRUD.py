from django.contrib.auth.models import User
from .models import Games, Teams, TeamMembers


def get_user(username):
    db_user = User.objects.filter(username=username).first()
    return db_user


def get_user_by_id(user_id):
    db_user = User.objects.filter(id=user_id).first()
    return db_user


def create_user(user):
    db_user = User(username=user["username"], password=user["password"])
    db_user.save()


def get_game_by_id(game_id):
    db_game = Games.objects.filter(id=game_id).first()
    return db_game


def create_game(game):
    db_game = Games(name=game["name"], description=game["description"], max_team_size=game["max_team_size"], game_admmin_id=game["game_admmin_id"])
    db_game.save()


def get_game_filered_by_team_id(game_id, team_id):
    db_game = Games.objects.filter(id=game_id, teams__id=team_id).first()
    return db_game


def update_game(game):
    db_game = Games.objects.filter(name=game["name"]).first()
    db_game.description = game["description"]
    db_game.max_team_size = game["max_team_size"]
    db_game.game_admmin_id = game["game_admmin_id"]
    db_game.save()
    return db_game


def create_team(team, members):
    try:
        team.save()
    except:
        raise Exception("Team with this name already exists")
    try:
        for member in members:
            db_team_member = TeamMembers(user_id=member, team_id=team.id)
            db_team_member.save()
    except:
        raise Exception("Error while adding team members")
    return team
