from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from .permissions import *
from .models import User
from .serializers import ReadUserSerializer, UserCreateSerializer, UserUpdateSerializer
from django.http import FileResponse, Http404
import os

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    print(f"Attempting login with email: {email}")  # Логирование email
    user = authenticate(request, username=email, password=password)

    if (user is not None) and user.is_superuser:
        login(request, user)

        return Response({
            'message': 'Successfully logged in!',
        }, status=status.HTTP_200_OK)

        # Если аутентификация не удалась
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def test_admin(request):
    return Response({
        'message': 'Successful test!',
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_logout_view(request):
    logout(request)  # Удаляет сессию и cookie с браузера пользователя
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def login_page(request):
    return render(request, 'admin_login.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def custom_admin_view(request):
    if not request.user.is_authenticated:
        return redirect('/u/a/login/')
    return render(request, 'administration.html')

@api_view(['GET'])
@permission_classes([IsAdminUser])
def download_logs(request):
    log_file_path = os.path.join('logs', 'async_log.log')
    if os.path.exists(log_file_path):
        response = FileResponse(open(log_file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="logs.log"'
        return response
    raise Http404("Log file not found.")

