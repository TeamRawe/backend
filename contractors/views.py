from .models import *
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from users.permissions import *
from database.logger import logger
from .tasks import get_company_task


@permission_classes([IsAuthenticated])
class SubContractorViewSet(viewsets.ModelViewSet):
    queryset = SubContractor.objects.all()
    serializer_class = SubContractorSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя. Администратор от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class GovernmentalCompanyViewSet(viewsets.ModelViewSet):
    queryset = GovernmentalCompany.objects.all()
    serializer_class = GovernmentalCompanySerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class ContactFaceViewSet(viewsets.ModelViewSet):
    queryset = ContactFace.objects.all()
    serializer_class = ContactFaceSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        user = request.user
        logger.info(f"Запрос на получение данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Частичное обновление данных пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        user = request.user
        logger.warning(f"Попытка удаления пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Создание нового пользователя от {user.email} с ролью {user.role} от {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required_fbv(['ADMIN', 'PROJECT_MANAGER', 'RULER'])
def get_company_api(request, id):
    get_company_task.delay(id)
    return Response({"detail": "Запрос отправлен"}, status=status.HTTP_202_ACCEPTED)


