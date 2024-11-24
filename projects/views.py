from users.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.exceptions import MethodNotAllowed


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN'])
@assignment_required(['ACTIVE', 'FREEZED'])
def test_assign(request, project_id, stage_id):
    user = request.user
    return Response({"message": f"Hello, {user.first_name}! You are allowed on this target"})


@permission_classes([IsAuthenticated])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProjectSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateProjectSerializer
        return ReadProjectSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE",
                               detail="Удаление запрещено")
    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
@permission_classes([IsAuthenticated])
class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateStageSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateStageSerializer
        return ReadStageSerializer
    @role_required(['ADMIN','PROJECT_MANAGER','STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE','FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @role_required(['ADMIN','PROJECT_MANAGER',])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER',])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE",
                               detail="Удаление запрещено")

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFileSerializer
        elif self.action in ['update', 'partial_update']:
            return CreateFileSerializer  # Используем тот же сериализатор для обновления
        return ReadFileSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','STAGE_MANAGER','RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER','STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER','STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление файлов запрещено")


@permission_classes([IsAuthenticated])
class ProjectAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectAssignment.objects.all()
    serializer_class = ProjectAssignmentSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление назначений запрещено")


@permission_classes([IsAuthenticated])
class StageAssignmentViewSet(viewsets.ModelViewSet):
    queryset = StageAssignment.objects.all()
    serializer_class = StageAssignmentSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER','RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление назначений запрещено")