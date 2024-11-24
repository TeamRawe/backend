from rest_framework import serializers
from .models import User

# Просмотр
class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'father_name', 'passport',
            'phone', 'email', 'role', 'is_active'
        ]
        read_only_fields = ['id']  # id будет доступен только для чтения

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'father_name', 'passport',
            'phone', 'email', 'password', 'role'
        ]

    def create(self, validated_data):
        # Извлекаем пароль и остальные данные
        password = validated_data.pop('password')
        # Используем UserManager для создания пользователя
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'father_name', 'passport',
            'phone', 'email', 'role', 'is_active'
        ]
        read_only_fields = ['email']  # email нельзя изменить после создания