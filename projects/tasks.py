import os
from tools.ms.ms_project_parser import *
from celery import shared_task
from django.core.mail import send_mail
from database.settings import EMAIL_HOST_USER
import json
from datetime import datetime
from decimal import Decimal
from users.models import User

@shared_task
def process_project_file(file_path):
    from .models import Project, Stage
    """Задача Celery для обработки XML-файла."""
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}

    # Обработка файла
    try:
        result_file = parse_ms_project(file_path)
        data = json.loads(result_file)
        # Основная (смрадная) магия
        project_data = {
            'title': data.get('ProjectName', ''),
            'start_date': datetime.strptime(data['Tasks'][0]['Start'], '%Y-%m-%dT%H:%M:%S').date(),
            # Дата начала на основе первой задачи
            'end_date': datetime.strptime(data['Tasks'][-1]['Finish'], '%Y-%m-%dT%H:%M:%S').date(),
            # Дата окончания на основе последней задачи
            'planned_cost': Decimal(data.get('TotalCost', 0)),
            # Пример: предполагаем, что есть поле для общего бюджета, но нужно его создать в JSON
            'customer': None,  # Получаем заказчика
            'progress': 0,  # Можно вычислить по проценту выполнения задач, но пока ставим 0
            'status': Project.ProjectStatus.PLANNED,  # Запланирован

        }
        # Создаем проект
        project = Project(**project_data)
        project.save()

        for task in data['Tasks']:
            # Дата начала и окончания
            start_date = datetime.strptime(task['Start'], '%Y-%m-%dT%H:%M:%S').date()
            end_date = datetime.strptime(task['Finish'], '%Y-%m-%dT%H:%M:%S').date()

            stage_data = {
                'project': project,
                'title': task['Name'],
                'start_date': start_date,
                'end_date': end_date,
                'planned_cost': Decimal(task['Cost']),
                'worker': None,
                # Мы предполагаем, что организация является подрядчиком
                'progress': 0,
                'status': Stage.StageStatus.PLANNED,
                # Статус можно установить как 'PLANNED' или 'ACTIVE' в зависимости от данных
                'created_by': project.created_by  # Пользователь, создавший проект
            }

            # Создаем этап
            stage = Stage(**stage_data)
            stage.save()
        return project

    except Exception as e:
        return {"status": "error", "message": str(e)}

@shared_task
def send_cluster_email_notification(subject, message, recipient_list=None):
    """
    Отправка уведомления на почту через Celery.
    """
    if recipient_list is None:
        recipient_list = list(User.objects.filter(role=User.Role.ADMIN).values_list('email', flat=True)) + \
                         list(User.objects.filter(role=User.Role.RULER).values_list('email', flat=True))

    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,  # ваш email отправителя
        recipient_list,
        fail_silently=False,
    )
