# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from projects.models import ProjectReport, StageReport, ProjectAssignment
# from users.tasks import send_email_notification  # Задача для отправки email
# from users.models import User
#
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from projects.models import ProjectReport, StageReport, ProjectAssignment, StageAssignment
# from .tasks import send_email_notification
# from users.models import User
#
#
# def send_notification_to_roles(report_instance, project=None, stage=None):
#     print("2")
#     """
#     Отправка уведомлений для ProjectReport и StageReport.
#     Если это ProjectReport - уведомляем PROJECT_MANAGER и RULER.
#     Если это StageReport - уведомляем STAGE_MANAGER, PROJECT_MANAGER, RULER.
#     """
#
#     recipient_emails = set()
#
#     # Если передан проект, отправляем PROJECT_MANAGER и RULER
#     if project:
#         project_assignments = ProjectAssignment.objects.filter(
#             project=project,
#             role__in=[User.Role.PROJECT_MANAGER, User.Role.RULER]
#         )
#         project_emails = [assignment.user.email for assignment in project_assignments if assignment.user.email]
#         recipient_emails.update(project_emails)
#
#     # Если передан этап, добавляем STAGE_MANAGER
#     if stage:
#         stage_assignments = StageAssignment.objects.filter(
#             stage=stage,
#             role=User.Role.STAGE_MANAGER
#         )
#         stage_emails = [assignment.user.email for assignment in stage_assignments if assignment.user.email]
#         recipient_emails.update(stage_emails)
#
#     # Добавляем всех администраторов
#     admins = User.objects.filter(role=User.Role.ADMIN).values_list('email', flat=True)
#     recipient_emails.update(admins)
#
#     if recipient_emails:
#         # Формируем письмо
#         subject = "Статус отчета изменен"
#         message = f"""
#         Статус отчета (ID: {report_instance.pk}) был изменен.
#         Новый статус: {report_instance.status}
#         """
#
#         # Отправляем письма через Celery
#         send_email_notification.delay(
#             subject,
#             message,
#             'your_email@yandex.ru',  # Укажите отправителя
#             list(recipient_emails)  # Преобразуем в список
#         )
#
#
# @receiver(pre_save, sender=ProjectReport)
# def notify_project_report_status_change(sender, instance, **kwargs):
#     print("1")
#     """
#     Сигнал для отправки уведомлений при изменении статуса ProjectReport.
#     """
#     # Если объект уже существует в БД
#     if instance.pk:
#         previous = sender.objects.get(pk=instance.pk)
#         if previous.status != instance.status:
#             send_notification_to_roles(instance, project=instance.project)
#
#
# @receiver(pre_save, sender=StageReport)
# def notify_stage_report_status_change(sender, instance, **kwargs):
#     print("1")
#     """
#     Сигнал для отправки уведомлений при изменении статуса StageReport.
#     """
#     # Если объект уже существует в БД
#     if instance.pk:
#         previous = sender.objects.get(pk=instance.pk)
#         if previous.status != instance.status:
#             send_notification_to_roles(instance, stage=instance.stage)
