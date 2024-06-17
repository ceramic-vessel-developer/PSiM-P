from django.contrib.auth.models import User
from .models import Games, Teams, TeamMembers, Checkpoints, Achievements


def get_user(username):
    db_user = User.objects.filter(username=username).first()
    return db_user


def get_user_by_id(user_id):
    db_user = User.objects.filter(id=user_id).first()
    return db_user


def create_user(user):
    db_user = User.objects.create_user(username=user["username"], password=user["password"])
    return db_user


def get_game_by_id(game_id):
    db_game = Games.objects.filter(id=game_id).first()
    db_game.checkpoints = Checkpoints.objects.filter(game_id=game_id)
    db_game.achievements = Achievements.objects.filter(game_id=game_id)
    return db_game


def create_game(game, achievements, checkpoints):
    db_game = Games(name=game["name"], description=game["description"], max_team_size=game["max_team_size"], game_admmin_id=game["game_admmin_id"])
    db_game.save()
    for achievement in achievements:
        db_achievement = Achievements(description=achievement["description"], bonus=achievement["bonus"], treshold=achievement["treshold"], checkpoint_id=achievement["checkpoint_id"], game_id=db_game.id)
        db_achievement.save()
    last_checkpoint_id = None
    for checkpoint in checkpoints:
        db_checkpoint = Checkpoints(name=checkpoint["name"], description=checkpoint["description"], qr_code_path=checkpoint["qr_code_path"], game_id=db_game.id, previous_id=last_checkpoint_id)
        db_checkpoint.save()
        last_checkpoint_id = db_checkpoint.id


def get_game_filered_by_team_id(game_id, team_id):
    db_game = Games.objects.filter(id=game_id, teams__id=team_id).first()
    db_game.checkpoints = Checkpoints.objects.filter(game_id=game_id)
    db_game.achievements = Achievements.objects.filter(game_id=game_id)
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
