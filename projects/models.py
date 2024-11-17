from django.db import models
import uuid
import mimetypes
from contractors.models import *
from django.core.validators import FileExtensionValidator
from database.settings import ALLOWED_FILE_EXTENSIONS
from datetime import datetime


# Create your models here.

class File(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    project = models.ForeignKey(
        'Project', on_delete=models.PROTECT, related_name='files', null=False, blank=False
    )
    stage = models.ForeignKey(
        'Stage', on_delete=models.PROTECT, related_name='files', null=True, blank=True
    )

    class FileCategory(models.TextChoices):
        IMAGE = 'IMAGE', 'Изображение'
        TABLE = 'TABLE', 'Таблица'
        DOCUMENT = 'DOCUMENT', 'Текстовые и PDF файлы'
        OTHER = 'OTHER', 'Прочие файлы'

    category = models.CharField(
        max_length=20, choices=FileCategory.choices, blank=True, null=True, help_text="Категория файла"
    )

    def dynamic_file_path(instance, filename):
        """Динамически генерирует путь для загрузки файла"""
        # Если файл привязан к проекту
        if instance.project:
            identifier = instance.project.id
            category = 'projects'
        # Если файл привязан к этапу
        elif instance.stage:
            identifier = instance.stage.id
            category = 'stages'
        else:
            identifier = 'unknown'
            category = 'misc'

        date_path = datetime.now().strftime('%Y/%m/%d')
        return f'{category}/{identifier}/{date_path}/{filename}'

    file = models.FileField(
        upload_to=dynamic_file_path,
        blank=True,
        null=True,
        help_text='Документы этапа',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_FILE_EXTENSIONS)]
    )

    def recognise_filetype(self, filename):

        mime_type, encoding = mimetypes.guess_type(filename)

        if not mime_type:
            return self.FileCategory.OTHER

        if mime_type.startswith('image'):
            return self.FileCategory.IMAGE
        elif mime_type.startswith('application/pdf') or mime_type in ['application/msword',
                                                                      'application/vnd.openxmlformats-officedocument'
                                                                      '.wordprocessingml.document']:
            return self.FileCategory.DOCUMENT
        elif mime_type.startswith('application/vnd.ms-excel') or mime_type.startswith(
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
            return self.FileCategory.TABLE
        else:
            return self.FileCategory.OTHER

    def save(self, *args, **kwargs):
        """Переопределяем метод сохранения для автоматической категоризации."""
        # Автоматически определяем категорию при сохранении
        if not self.category:
            self.category = self.recognise_filetype(self.file.name)

        # TODO: В будущем добавим проверку на вирусы через magic (redis + celery)
        # Проверка на вирусы будет выполняться здесь перед сохранением

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.file.name}'


class Project(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text='Полное наименование организации'
    )
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    planned_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Плановый бюджет')
    # Связь с госкомпанией - заказчиком проекта
    customer = models.ForeignKey(GovernmentalCompany, on_delete=models.PROTECT, related_name="projects")

    class ProjectStatus(models.TextChoices):
        ARCHIVED = 'ARCHIVED', 'В архиве'
        APPROVED = 'APPROVED', 'Проект сдан'
        FINISHED = 'FINISHED', 'Работы выполнены'
        ACTIVE = 'ACTIVE', 'Активный'
        AWAITING = 'Ожидается начало работ'
        PLANNED = 'Запланирован'

    status = models.CharField(
        max_length=25,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNED,
        help_text='Состояние проекта'
    )

    def __str__(self):
        return self.title


class Stage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="stages",
                                help_text='Проект этого этапа')

    parent_stage = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children_stages',
        help_text='Родительский этап'
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    planned_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class StageStatus(models.TextChoices):
        APPROVED = 'APPROVED', 'Проект сдан'
        FINISHED = 'FINISHED', 'Работы выполнены'
        ACTIVE = 'ACTIVE', 'Активный'
        AWAITING = 'Ожидается начало работ'
        PLANNED = 'Запланирован'

    status = models.CharField(
        max_length=25,
        choices=StageStatus.choices,
        default=StageStatus.PLANNED,
        help_text='Состояние этапа'
    )

    number = models.CharField(max_length=20, blank=True, null=False)

    def save(self, *args, **kwargs):
        # Генерация номера этапа
        if not self.number:  # Если номер этапа ещё не задан (например, при создании)
            if self.parent_stage:
                # Если у этапа есть родитель, то добавляем номер к номеру родительского этапа
                parent_stage_number = self.parent_stage.number
                # Формируем номер для подэтапа
                self.number = f"{parent_stage_number}.{len(self.parent_stage.children_stages.all()) + 1}"
            else:
                # Если это основной этап, просто присваиваем номер "1"
                self.number = "1"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.number} {self.name}'