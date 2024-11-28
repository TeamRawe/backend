from celery import shared_task
from django.core.mail import send_mail
from database.settings import EMAIL_HOST_USER

@shared_task
def send_email_notification(subject, message, email, recipient_list):
    """
    Отправка уведомления на почту через Celery.
    """
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,  # ваш email отправителя
        recipient_list,
        fail_silently=False,
    )