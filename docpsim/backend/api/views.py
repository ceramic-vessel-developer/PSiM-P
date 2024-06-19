from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from . import CRUD, serializers
from .models import Games, Teams, TeamMembers, Checkpoints, Unlocked, Comments


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    user = serializers.UserCreate(data=request.data)
    user.is_valid(raise_exception=True)
    existing_user = CRUD.get_user(user.validated_data["username"])
    if existing_user:
        return Response({"detail": "Email already registered"}, status=400)

    CRUD.create_user(user.validated_data)

    return Response({"message": "user created successfully"}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_users_me(request):
    return Response(serializers.UserReturn(request.user).data)


@api_view(['GET', 'DELETE'])
def user(request, id):
    db_user = CRUD.get_user_by_id(id)
    if db_user is None:
        return Response({"detail": "User not found"}, status=404)
    if request.method == 'DELETE':
        try:
            db_user.delete()
        except:
            return Response({"detail": "Could not delete user"}, status=400)
        return Response({"message": "user deleted successfully"})
    return Response(serializers.UserReturn(db_user).data)


@api_view(['GET'])
def read_game(request, id):
    db_game = CRUD.get_game_by_id(id)
    if db_game is None:
        return Response({"detail": "Game not found"}, status=404)
    return Response(serializers.GameReturnAll(db_game).data)


@api_view(['POST', 'PUT'])
def games(request):
    if request.method == 'PUT':
        return update_game(request)
    return create_game(request)


def create_game(request):
    game = serializers.GameCreate(data=request.data["game"])
    game.is_valid(raise_exception=True)
    checkpoints = serializers.CheckpointCreate(data=request.data["checkpoints"], many=True)
    checkpoints.is_valid(raise_exception=True)
    achievements = serializers.AchievementCreate(data=request.data["achievements"], many=True)
    achievements.is_valid(raise_exception=True)
    id = CRUD.create_game(game.validated_data, checkpoints.validated_data, achievements.validated_data)
    return Response({"id": id}, status=201)


@api_view(['GET'])
def read_game_user(request, game_id, user_id):
    db_game = CRUD.get_game_filered_by_team_id(game_id, user_id)
    if db_game is None:
        return Response({"detail": "Game not found"}, status=404)
    return Response(serializers.GameReturn(db_game).data)


def update_game(request):
    game = serializers.GameCreate(data=request.data)
    game.is_valid(raise_exception=True)
    CRUD.update_game(game.validated_data)
    return Response(status=201)


@api_view(['GET', 'POST'])
def comments(request, checkpoint_id):
    if request.method == 'POST':
        comment = serializers.CommentsCreate(data=request.data)
        comment.is_valid(raise_exception=True)
        db_comment = Comments(comment=comment.validated_data["comment"], author_id=comment.validated_data["user_id"],
                              checkpoint_id=checkpoint_id, date_time=timezone.now())
        db_comment.save()
        return Response({"message": "comment created successfully"}, status=201)
    db_comments = Comments.objects.filter(checkpoint_id=checkpoint_id)
    return Response(serializers.Comments(db_comments, many=True).data)


@api_view(['PUT'])
def unlock_checkpoint(request, checkpoint_id, team_id):
    db_duplicate = Unlocked.objects.filter(checkpoint_id=checkpoint_id, team_id=team_id).first()
    if db_duplicate:
        return Response({"detail": "Checkpoint already unlocked"}, status=400)
    db_checkpoint = Checkpoints.objects.filter(id=checkpoint_id).first()
    db_previous = Checkpoints.objects.filter(id=db_checkpoint.previous_id).first()

    if not db_previous or Unlocked.objects.filter(checkpoint_id=db_previous.id, team_id=team_id).first():
        db_unlocked = Unlocked(checkpoint_id=checkpoint_id, team_id=team_id)
        try:
            db_unlocked.save()
        except:
            return Response({"detail": "Database error"}, status=400)
        return Response({"message": "checkpoint unlocked successfully"}, status=201)
    else:
        return Response({"detail": "Previous checkpoint not unlocked"}, status=400)


@api_view(['GET', 'POST'])
def teams(request, game_id):
    if request.method == 'POST':
        team = serializers.TeamCreate(data=request.data)
        team.is_valid(raise_exception=True)
        db_team = Teams(game_id=game_id, name=team.validated_data["name"], points=0, game_times=[])
        CRUD.create_team(db_team, team.validated_data["players"])
        return Response({"message": "team created successfully"}, status=201)
    db_teams = Teams.objects.filter(game_id=game_id)
    return Response(serializers.TeamReturn(db_teams).data)


@api_view(['GET'])
def read_team(request, team_id):
    db_team = Teams.objects.filter(id=team_id).first()
    db_team.members = TeamMembers.objects.filter(team_id=team_id).values_list('user_id', flat=True)
    return Response(serializers.TeamReturn(db_team).data)


@api_view(['GET'])
def read_games_admin(request, user_id):
    db_games = Games.objects.filter(game_admin_id=user_id)
    return Response(serializers.GameReturnStrip(db_games, many=True).data)


@api_view(['GET'])
def read_games_player(request, user_id):
    db_team_members = TeamMembers.objects.filter(user_id=user_id)
    db_teams = []
    for member in db_team_members:
        db_team = Teams.objects.filter(id=member.team_id).first()
        db_teams.append(db_team)
    db_games = []
    for team in db_teams:
        db_game = Games.objects.filter(id=team.game_id).first()
        db_games.append(db_game)
    return Response(serializers.GameReturnStrip(db_games, many=True).data)


@api_view(['GET'])
def read_checkpoint_player(request, checkpoint_id):
    db_checkpoint = Checkpoints.objects.filter(id=checkpoint_id).first()
    return Response(serializers.CheckpointReturn(db_checkpoint).data)


@api_view(['GET'])
def read_checkpoint_admin(request, checkpoint_id):
    db_checkpoint = Checkpoints.objects.filter(id=checkpoint_id).first()
    return Response(serializers.CheckpointReturnAdmin(db_checkpoint).data)


@api_view(['GET'])
def read_team_id(request, game_id, user_id):
    team_id = -1
    db_teams = Teams.objects.filter(game_id=game_id)
    for team in db_teams:
        db_members = TeamMembers.objects.filter(user_id=user_id, team_id=team.id).first()
        if db_members:
            team_id = team.id
            break
    if team_id == -1:
        return Response({"detail": "Nie znaleziono zespołu"}, status=404)
    db_team = Teams.objects.filter(id=team_id).first()
    return Response(serializers.TeamReturnShort(db_team).data)
