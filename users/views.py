from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from database.settings import DEBUG
from rest_framework_simplejwt.exceptions import TokenError
from .role_restrictons import *



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    print(f"Attempting login with email: {email}")  # Логирование email
    user = authenticate(request, username=email, password=password)

    if user is not None:
        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        # noinspection PyUnresolvedReferences
        access_token: str = str(refresh.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'role': user.role,
        }, status=200)

        # Если аутентификация не удалась
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    return Response({"message": "Successful test"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_test(request):
    return Response({"message": "Successful secure test"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])  # Этот endpoint доступен всем, чтобы обновить токен
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)

        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)

        return Response({
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
        }, status=200)



    except TokenError:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN'])
def test_role(request):
    user = request.user
    # noinspection PyUnresolvedReferences
    return Response({"message": f"Hello, {user.first_name}! Your role: {user.role} This was a test."})
