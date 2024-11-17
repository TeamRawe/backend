from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class ContactFace(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        help_text='Контактный телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text='Электронная почта'
    )
    name = models.CharField(max_length=255, blank=False, Null=False)

    def __str__(self):
        return self.name


class SubContractor(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text='Полное наименование организации'
    )
    inn = models.CharField(
        max_length=12,
        blank=False,
        null=True,
        help_text='ИНН - Идентификационный номер налогоплательщика'
    )
    ogrn = models.CharField(
        max_length=13,
        blank=False,
        null=False,
        help_text='ОГРН - Основной государственный регистрационный номер'
    )
    phone = PhoneNumberField(
        blank=False,
        null=False,
        help_text='Контактный телефон'
    )
    email = models.EmailField(
        blank=False,
        null=False,
        help_text='Электронная почта'
    )
    contact_faces = models.ManyToManyField(
        ContactFace,  # Модель ContactFace, связь многие ко многим
        related_name='contractors',  # Связь в обратную сторону (с ContactFace)
        blank=True,  # Свободное добавление контактных лиц, если они есть
        help_text='Контактные лица'
    )

    def __str__(self):
        return self.title


class GovernmentalCompany(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text='Полное наименование организации'
    )

    address = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text='Адрес'
    )

    okfs = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='ОКФС - Форма собственности'
    )
    okopf = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ОКОПФ - Организационно-правовая форма'
    )
    okogu = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ОКОГУ - Орган государственного управления'
    )
    inn = models.CharField(
        max_length=12,
        blank=False,
        null=False,
        help_text='ИНН - Идентификационный номер налогоплательщика'
    )
    ogrn = models.CharField(
        max_length=13,
        blank=False,
        null=False,
        help_text='ОГРН - Основной государственный регистрационный номер'
    )
    kpp = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        help_text='КПП - Код причины постановки на учет'
    )
    okato = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ОКАТО - Код территории'
    )
    okpo = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='ОКПО - Общероссийский классификатор предприятий и организаций'
    )
    oktmo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ОКТМО - Общероссийский классификатор территорий муниципальных образований'
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        help_text='Контактный телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text='Электронная почта'
    )
    website = models.URLField(
        blank=True,
        null=True,
        help_text='Сайт компании'
    )
    contact_faces = models.ManyToManyField(
        ContactFace,  # Модель ContactFace, связь многие ко многим
        related_name='contractors',  # Связь в обратную сторону (с ContactFace)
        blank=True,  # Свободное добавление контактных лиц, если они есть
        help_text='Контактные лица'
    )

    def __str__(self):
        return self.title
