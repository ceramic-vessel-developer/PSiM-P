from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register', views.register),
    path('login/', TokenObtainPairView.as_view()),
    path('users/me/', views.read_users_me),
]
