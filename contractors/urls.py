from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

subcontractor_router = DefaultRouter()
subcontractor_router.register(r'projects', views.SubContractorViewSet, basename='subcontractor')

governmental_company_router = DefaultRouter()
governmental_company_router.register(r'governmental-companies', views.GovernmentalCompanyViewSet, basename='governmental_company')

contact_face_router = DefaultRouter()
contact_face_router.register(r'contact-faces', views.ContactFaceViewSet, basename='contact_face')

urlpatterns = [
    path('', include(subcontractor_router.urls)), # Подрядчики
    path('', include(governmental_company_router.urls)), # Гос компании
    path('', include(contact_face_router.urls)), # Контактные лица
]