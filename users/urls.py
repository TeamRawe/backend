from django.urls import path
from . import views

# API
urlpatterns = [
    path('login/', views.login, name='login'),  # Ручка логина
    path('test/', views.test, name='test'), # Тест
    path('secure_test/', views.secure_test, name='secure_test'), # Тест требующий JWT
    path('refresh/', views.refresh_token, name='refresh') #Новый access_token токен по refresh_token
]
