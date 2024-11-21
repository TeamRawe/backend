from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from projects.models import ProjectAssignment, StageAssignment

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

            # Проверка назначения на этап
            if stage_id:
                stage_assignment = StageAssignment.objects.filter(
                    target__id=stage_id,
                    user=user,
                    status__in=allowed_statuses  # Проверка по списку допустимых статусов
                ).first()
                if not stage_assignment:
                    print(1)
                    return Response(
                        status=status.HTTP_403_FORBIDDEN
                        # TODO: добавить логирование
                    )
            else:
                # Проверка назначения на проект
                if project_id:
                    project_assignment = ProjectAssignment.objects.filter(
                        target__id=project_id,
                        user=user,
                        status__in=allowed_statuses  # Проверка по списку допустимых статусов
                    ).first()
                    if not project_assignment:
                        print(2)
                        return Response(
                            status=status.HTTP_403_FORBIDDEN
                        )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator



