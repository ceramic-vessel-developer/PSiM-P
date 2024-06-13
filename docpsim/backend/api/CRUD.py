from django.contrib.auth.models import User


def get_user(username):
    db_user = User.objects.filter(username=username).first()
    return db_user


def create_user(user):
    db_user = User(username=user["username"], password=user["password"])
    db_user.save()
