from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import CRUD, serializers


@api_view(['POST'])
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
