# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import StageReport, ProjectReport
# from database.logger import logger
#
# @receiver(post_save, sender=StageReport)
# def track_status_change_stage_report(sender, instance, **kwargs):
#     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#     # Проверяем, изменился ли статус
#     if instance.pk:
#         old_instance = StageReport.objects.get(pk=instance.pk)
#         if old_instance.status != instance.status:
#             logger.info(f"Status of StageReport (ID: {instance.id}) changed from {old_instance.status} to {instance.status} by {instance.created_by}")
#             print(f"Status of StageReport (ID: {instance.id}) changed from {old_instance.status} to {instance.status} by {instance.created_by}")
#
# @receiver(post_save, sender=ProjectReport)
# def track_status_change_project_report(sender, instance, **kwargs):
#     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#     # Проверяем, изменился ли статус
#     if instance.pk:
#         old_instance = ProjectReport.objects.get(pk=instance.pk)
#         if old_instance.status != instance.status:
#             logger.info(f"Status of ProjectReport (ID: {instance.id}) changed from {old_instance.status} to {instance.status} by {instance.created_by}")
#             print(f"Status of ProjectReport (ID: {instance.id}) changed from {old_instance.status} to {instance.status} by {instance.created_by}")