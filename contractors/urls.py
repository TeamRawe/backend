from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import get_company_api

subcontractor_router = DefaultRouter()
subcontractor_router.register(r'subs', views.SubContractorViewSet, basename='subcontractor')

governmental_company_router = DefaultRouter()
governmental_company_router.register(r'govs', views.GovernmentalCompanyViewSet, basename='governmental_company')

contact_face_router = DefaultRouter()
contact_face_router.register(r'contacts', views.ContactFaceViewSet, basename='contact_face')

urlpatterns = [
    path('', include(subcontractor_router.urls)), # Подрядчики
    path('', include(governmental_company_router.urls)), # Гос компании
    path('', include(contact_face_router.urls)), # Контактные лица
    path('gov_reg/<int:id>', get_company_api, name="get_company"),
]