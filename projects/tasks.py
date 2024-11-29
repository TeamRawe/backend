import os
from tools.ms.ms_project_parser import *
from celery import shared_task
from django.core.mail import send_mail
from database.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def process_project_file(file_path):
    """Задача Celery для обработки XML-файла."""
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}

    # Обработка файла
    try:
        result_file = parse_ms_project(file_path)
        return {"status": "success", "output_file": result_file}
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
