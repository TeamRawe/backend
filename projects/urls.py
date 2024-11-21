from django.urls import path
from . import views

# API
urlpatterns = [
    path('test_assign/<uuid:project_id>/<uuid:stage_id>/', views.test_assign, name='test_assign'),
    # Тест принадлежности пользователя к данной сущности
]
