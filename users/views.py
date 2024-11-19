from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from database.settings import DEBUG
from rest_framework_simplejwt.exceptions import TokenError


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

        response = Response({
            'user_id': user.id,
            'role': user.role,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=not(DEBUG),
            secure=True,  # Устанавливаем True в production для HTTPS
            samesite='Lax',  # Опция безопасности для ограничения cookies к тем же сайтам
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=not(DEBUG),
            secure=True,  # Устанавливаем True в production для HTTPS
            samesite='Lax',  # Опция безопасности для ограничения cookies к тем же сайтам
        )

        return response

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
    refresh_token = request.COOKIES.get('refresh_token')  # Получаем refresh token из cookies

    if not refresh_token:
        return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Создаём объект RefreshToken из refresh_token
        refresh = RefreshToken(refresh_token)

        # Генерируем новые access и refresh токены
        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)

        # Отправляем новые токены в cookies
        response = Response({ 'detail': 'New tokens have been sent'})

        # Устанавливаем новые токены в cookies с актуальными сроками жизни
        response.set_cookie('access_token', new_access_token, httponly=not(DEBUG), secure=True)
        response.set_cookie('refresh_token', new_refresh_token, httponly=not(DEBUG), secure=True)

        return response

    except TokenError:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
