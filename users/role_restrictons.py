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

def assignment_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        #Подсасывваем пользователя
        user = request.user

        # Извлекаем ID проекта или этапа из URL-параметров
        project_id = kwargs.get('project_id')  # Получаем project_id из URL
        stage_id = kwargs.get('stage_id')  # Получаем stage_id из URL (если нужно)

        if stage_id:
            stage_assignment = StageAssignment.objects.filter(
                target__id=stage_id,
                user=user,
                status=StageAssignment.AssignmentStatus.ACTIVE
            ).first()
            if not stage_assignment:
                return Response(
                    {"detail": "Access denied. User is not assigned to this stage."},
                    status=status.HTTP_403_FORBIDDEN
                )

        if project_id:
            project_assignment = ProjectAssignment.objects.filter(
                target__id=project_id,
                user=user,
                status=ProjectAssignment.AssignmentStatus.ACTIVE
            ).first()
            if not project_assignment:
                return Response(
                    {"detail": "Access denied. User is not assigned to this project."},
                    status=status.HTTP_403_FORBIDDEN
                )

            #TODO: доделать это с правильной логикой




