from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register', views.register),
    path('login/', TokenObtainPairView.as_view()),
    path('users/me/', views.read_users_me),
    path('users/<int:id>', views.user),
    path('games', views.create_game),
    path('games/update', views.update_game),
    path('games/<int:id>', views.read_game),
    path('games/<int:game_id>/team/<int:team_id>', views.read_game_team),
    path('games/users/<int:user_id>/admin', views.read_games_admin),
    path('games/users/<int:user_id>/player', views.read_games_player),
    path('checkpoint/<int:checkpoint_id>/comments', views.comments),
    path('checkpoint/<int:checkpoint_id>/team/<int:team_id>/unlock', views.unlock_checkpoint),
    path('checkpoints/<int:checkpoint_id>/player', views.read_checkpoint_player),
    path('checkpoints/<int:checkpoint_id>/admin', views.read_checkpoint_admin),
    path('teams/<int:game_id>', views.teams),
    path('teams/team/<int:team_id>', views.read_team),
    path('teams/<int:game_id>/<int:user_id>', views.read_team_id),
]
