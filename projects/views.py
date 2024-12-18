from users.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from .serializers import *
from rest_framework.exceptions import MethodNotAllowed
from database.logger import logger
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.decorators import action

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN'])
@assignment_required(['ACTIVE', 'FREEZED'])
def test_assign(request, project_id, stage_id):
    user = request.user
    logger.info(f"Запрос от пользователя {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
    logger.info(f"Параметры запроса: project_id = {project_id}, stage_id = {stage_id}")
    return Response({"message": f"Hello, {user.first_name}! You are allowed on this target"})


@permission_classes([IsAuthenticated])
class ProjectViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProjectSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateProjectSerializer
        return ReadProjectSerializer

    filterset_fields = ['status', 'created_by', 'start_date']  # Поля для фильтрации
    search_fields = ['name', 'description']  # Поля для поиска
    ordering_fields = ['start_date', 'end_date', 'name']

    # Кастомное действие для получения проектов, связанных с пользователем
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER'])
    def assigned(self, request):
        user = request.user

        # Получение проектов через модель назначений
        assigned_projects = Project.objects.filter(
            Q(assignments__assigned_to=user) |
            Q(assignments__project_manager=user)
        ).distinct()

        # Сериализация результатов
        serializer = self.get_serializer(assigned_projects, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)
    @role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE",
                               detail="Удаление запрещено")

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'created_by', 'start_date']  # Поля для фильтрации
    search_fields = ['name', 'description']  # Поля для поиска
    ordering_fields = ['start_date', 'end_date', 'name']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateStageSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateStageSerializer
        return ReadStageSerializer

    def perform_create(self, serializer):
        # Проверяем права и заполняем created_by текущим пользователем
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)
    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', ])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', ])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE",
                               detail="Удаление запрещено")

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['uploaded_at', 'created_by', 'project', 'stage']  # Добавлены project и stage
    search_fields = ['name', 'description']
    ordering_fields = ['uploaded_at', 'name']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFileSerializer
        elif self.action in ['update', 'partial_update']:
            return CreateFileSerializer  # Используем тот же сериализатор для обновления
        return ReadFileSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление файлов запрещено")

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class ProjectAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectAssignment.objects.all()
    serializer_class = ProjectAssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'assigned_to', 'project']  # Добавлены новые поля
    search_fields = ['assigned_to__email', 'project__name']
    ordering_fields = ['created_at', 'status']

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление назначений запрещено")

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class StageAssignmentViewSet(viewsets.ModelViewSet):
    queryset = StageAssignment.objects.all()
    serializer_class = StageAssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'assigned_to', 'stage']  # Добавлены новые поля
    search_fields = ['assigned_to__email', 'stage__name']
    ordering_fields = ['created_at', 'status']

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление назначений запрещено")

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class StageReportViewSet(viewsets.ModelViewSet):
    queryset = StageReport.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'created_by', 'stage']  # Добавлены поля фильтрации
    search_fields = ['description', 'stage__name']
    ordering_fields = ['created_at', 'status']

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return StageReportCreateSerializer
        return StageReportSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN'])
    @assignment_required(['ACTIVE', 'PROJECT_MANAGER', 'STAGE_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление отчетов запрещено")

    @role_required(['ADMIN'])  # Только администраторы могут получить список
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class ProjectReportViewSet(viewsets.ModelViewSet):
    queryset = ProjectReport.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'created_by', 'project']  # Добавлены поля фильтрации
    search_fields = ['description', 'project__name']
    ordering_fields = ['created_at', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectReportCreateSerializer
        return ProjectReportSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пользователь должен быть аутентифицирован")
        serializer.save(created_by=self.request.user)

    @role_required(['ADMIN', 'PROJECT_MANAGER', 'STAGE_MANAGER', 'RULER'])
    @assignment_required(['ACTIVE', 'FREEZED'])
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN', 'PROJECT_MANAGER'])
    @assignment_required(['ACTIVE'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required([])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление отчетов по проекту запрещено")

    @role_required(['ADMIN'])  # Ограничение доступа к списку только для администраторов
    def list(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Запрос списка пользователей от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().list(request, *args, **kwargs)
