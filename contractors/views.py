from .models import *
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from users.permissions import *
@permission_classes([IsAuthenticated])
class SubContractorViewSet(viewsets.ModelViewSet):
    queryset = SubContractor.objects.all()
    serializer_class = SubContractorSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class GovernmentalCompanyViewSet(viewsets.ModelViewSet):
    queryset = GovernmentalCompany.objects.all()
    serializer_class = GovernmentalCompanySerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class ContactFaceViewSet(viewsets.ModelViewSet):
    queryset = ContactFace.objects.all()
    serializer_class = ContactFaceSerializer

    @role_required(['ADMIN', 'PROJECT_MANAGER','RULER','STAGE_MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        # Декоратор ограничит доступ для указанных ролей
        return super().retrieve(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Удаление субподрядчика запрещено. Вместо этого можно деактивировать субподрядчика.")

    @role_required(['ADMIN','PROJECT_MANAGER'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)