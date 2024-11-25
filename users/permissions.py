from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from projects.models import ProjectAssignment, StageAssignment
from rest_framework.exceptions import PermissionDenied


#Декоратор для ролей
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.role not in allowed_roles:
                return Response({"detail": "Access denied. Insufficient role."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def assignment_required(allowed_statuses):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            project_id = kwargs.get('project_id')
            stage_id = kwargs.get('stage_id')

            # Проверка на активный статус, роль ADMIN или RULER, а также суперпользователя
            if user.is_active and (user.is_superuser or user.role in ['ADMIN', 'RULER']):
                return view_func(request, *args, **kwargs)

            # Проверка назначения на этап
            if stage_id:
                stage_assignment = StageAssignment.objects.filter(
                    target__id=stage_id,
                    user=user,
                    status__in=allowed_statuses  # Проверка по списку допустимых статусов
                ).first()
                if not stage_assignment:
                    # TODO: добавить логирование
                    return Response(
                        status=status.HTTP_403_FORBIDDEN
                    )
            # Проверка назначения на проект
            elif project_id:
                project_assignment = ProjectAssignment.objects.filter(
                    target__id=project_id,
                    user=user,
                    status__in=allowed_statuses  # Проверка по списку допустимых статусов
                ).first()
                if not project_assignment:
                    # TODO: добавить логирование
                    return Response(
                        status=status.HTTP_403_FORBIDDEN
                    )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

'''
@role_required(['ADMIN','PROJECT_MANAGER', 'STAGE_MANAGER'])
@only_for_self(['STAGE_MANAGER'])
def perform_create(self, serializer):
        serializer.save()




'''


def only_for_self(allowed_roles):
    """
    Декоратор для проверки, что пользователь с указанными ролями
    взаимодействует только со своим профилем.
    """

    def decorator(view_func):
        def _wrapped_view(self, request, *args, **kwargs):
            # Проверяем, что пользователь аутентифицирован
            if not request.user.is_authenticated:
                raise PermissionDenied("Необходимо войти в систему.")

            # Проверяем, что роль пользователя входит в список ролей с ограничением
            if request.user.role in allowed_roles:
                # Получаем объект (например, пользователя), с которым работает метод
                obj = self.get_object()

                # Проверка: ID объекта должен совпадать с ID текущего пользователя
                if obj.id != request.user.id:
                    raise PermissionDenied()

            # Если проверка пройдена или роль пользователя не подлежит ограничению, вызываем оригинальный метод
            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator
