from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

# API
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Ручка логина
    path('test/', views.test, name='test'), # Тест
    path('secure_test/', views.secure_test, name='secure_test'), # Тест требующий авторизации
    path('logout/', views.logout_view, name='logout'), #Новый access_token токен по refresh_token
    path('role_test/', views.test_role, name='role_test'),
    path('check_session/', views.check_session, name='check_session'),
    path('', include(router.urls)),
    path('email/',views.send_email_test, name='email_test' )
]
