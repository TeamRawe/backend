from django.urls import path
from . import views

# API
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Ручка логина
    path('test/', views.test, name='test'), # Тест
    path('secure_test/', views.secure_test, name='secure_test'), # Тест требующий JWT
    path('logout/', views.logout_view, name='logout'), #Новый access_token токен по refresh_token
    path('role_test/', views.test_role, name='role_test'),
]
