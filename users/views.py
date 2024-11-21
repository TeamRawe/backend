from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .role_restrictons import *


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    print(f"Attempting login with email: {email}")  # Логирование email
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)

        return Response({
            'message': 'Successfully logged in!',
            'role': user.role,
        }, status=status.HTTP_200_OK)

        # Если аутентификация не удалась
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)  # Удаляет сессию и cookie с браузера пользователя
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    return Response({"message": "Successful test"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_test(request):
    return Response({"message": "Successful secure test"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN'])
def test_role(request):
    user = request.user
    # noinspection PyUnresolvedReferences
    return Response({"message": f"Hello, {user.first_name}! Your role: {user.role} This was a test."})
