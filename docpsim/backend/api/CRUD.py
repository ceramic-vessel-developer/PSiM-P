import segno
from django.conf import settings
from django.contrib.auth.models import User
from .models import Games, Teams, TeamMembers, Checkpoints, Unlocked, Achievements


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


def create_game(game, checkpoints, achievements):
    db_game = Games(name=game["name"], description=game["description"], max_team_size=game["max_team_size"],
                    game_admin_id=game["game_admin_id"])
    db_game.save()
    checkpoints_id = []
    for checkpoint in checkpoints:
        previous_id = checkpoints_id[checkpoint["previous"]] if checkpoint["previous"] != -1 else None
        db_checkpoint = Checkpoints(name=checkpoint["name"], description=checkpoint["description"],
                                    qr_code_path="mock", game_id=db_game.id, previous_id=previous_id)
        db_checkpoint.save()
        new_id = db_checkpoint.id
        qr_string = f"{settings.PROXY}/unlock/{db_game.id}/{new_id}"
        qr_code = segno.make_qr(qr_string)
        qr_path = settings.QR_PATH / f"qr_{new_id}.png"
        qr_code.save(str(qr_path), scale=10)
        db_checkpoint.qr_code_path = f"qr_{new_id}.png"
        db_checkpoint.save()
        checkpoints_id.append(new_id)

    for achievement in achievements:
        c_id = None
        if achievement["checkpoint_id"]:
            c_id = checkpoints_id[achievement["checkpoint_id"]]
        db_achievement = Achievements(description=achievement["description"], unlocked=False, bonus=achievement["bonus"],
                                      treshold=achievement["treshold"], checkpoint_id=c_id, game_id=db_game.id)
        db_achievement.save()

    return db_game.id


def get_game_filered_by_team_id(game_id, user_id):
    team_id = -1
    db_teams = Teams.objects.filter(game_id=game_id)
    for team in db_teams:
        db_members = TeamMembers.objects.filter(user_id=user_id, team_id=team.id).first()
        if db_members:
            team_id = team.id
            break
    db_game = Games.objects.filter(id=game_id).first()
    if db_game is None:
        return None
    db_game.achievements = Achievements.objects.filter(game_id=game_id)
    db_game.checkpoints_locked = list(Checkpoints.objects.filter(game_id=game_id))
    db_game.checkpoints_unlocked = []

    for checkpoint in db_game.checkpoints_locked:
        db_unlocked = Unlocked.objects.filter(checkpoint_id=checkpoint.id, team_id=team_id).first()
        if db_unlocked:
            db_game.checkpoints_unlocked.append(checkpoint)

    for checkpoint in db_game.checkpoints_unlocked:
        db_game.checkpoints_locked.remove(checkpoint)
    return db_game


def update_game(game):
    db_game = Games.objects.filter(name=game["name"]).first()
    db_game.description = game["description"]
    db_game.max_team_size = game["max_team_size"]
    db_game.game_admin_id = game["game_admin_id"]
    db_game.save()
    return db_game


def create_team(team, members):
    try:
        team.save()
    except:
        raise Exception("Team with this name already exists")
    try:
        for member in members:
            db_user = User.objects.filter(username=member).first()
            db_team_member = TeamMembers(team_id=team.id, user_id=db_user.id)
            db_team_member.save()
    except:
        raise Exception("Error while adding team members")
    return team
