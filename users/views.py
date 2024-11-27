from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import *
from .serializers import ReadUserSerializer, UserCreateSerializer, UserUpdateSerializer
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from .models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from database.logger import logger

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    print(f"Attempting login with email: {email}")  # Логирование email
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        logger.info(f"Успешная авторизация {user.email} от {request.META.get('REMOTE_ADDR')}")
        return Response({
            'message': 'Successfully logged in!',
            'id': user.id,
        }, status=status.HTTP_200_OK)

        # Если аутентификация не удалась
    logger.warn(f"Авторизация не удалась. Переданы данные {email, password} от {request.META.get('REMOTE_ADDR')}")
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)  # Удаляет сессию и cookie с браузера пользователя
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    logger.info(f"Токен CSRF успешно сгенерирован для {request.META.get('REMOTE_ADDR')}")
    csrf_token = get_token(request)  # Генерация CSRF токена
    response = JsonResponse({'message': 'CSRF cookie set successfully'})  # Ответ клиенту
    response.set_cookie(  # Устанавливаем токен в куки
        key='csrftoken',
        value=csrf_token,
        httponly=False,  # Не делаем токен HttpOnly, чтобы JavaScript мог его использовать (если нужно)
        secure=False,  # Включите True для HTTPS в продакшн
        samesite='Lax'  # Настройка SameSite для предотвращения CSRF атак
    )
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_test(request):
    return Response({"message": "Successful secure test"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN','RULER','PROJECT_MANAGER','STAGE_MANAGER'])
def test_role(request):
    user = request.user
    # noinspection PyUnresolvedReferences
    return Response({"message": f"Hello, {user.first_name}! Your role: {user.role} This was a test."})
@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return ReadUserSerializer
    @only_for_self(['STAGE_MANAGER', 'PROJECT_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ к методу retrieve для указанных ролей
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE",
                               detail="Удаление пользователя запрещено. Вместо этого можно деактивировать пользователя.")
    @role_required(['ADMIN'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)




