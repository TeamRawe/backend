'''
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Проверим, есть ли токен в cookies
        access_token = request.COOKIES.get('access_token')

        # Если токен найден, пытаемся его валидировать
        if access_token:
            try:
                validated_token = self.get_validated_token(access_token)
                user = self.get_user(validated_token)
                return (user, validated_token)
            except AuthenticationFailed:
                raise AuthenticationFailed('Invalid token')

        return None  # Если токен отсутствует, ничего не делаем

class AllowAnyCookie(AllowAny):
    def has_permission(self, request, view):
        # Не выполняем проверку аутентификации, если доступ разрешен для всех
        return True

# Создаем декоратор, который будет работать с AllowAnyCookie
def permission_classes_decorator(permission_classes):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for permission in permission_classes:
                if not permission().has_permission(request, None):
                    raise PermissionDenied("You do not have permission to access this resource.")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
'''




