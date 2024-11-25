from django.db import models
import uuid
from encrypted_model_fields.fields import EncryptedCharField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, last_name, phone, passport, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, first_name=first_name, last_name=last_name, phone=phone,
                          passport=passport, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, phone, passport, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role',User.Role.ADMIN)

        return self.create_user(email, password, first_name, last_name, phone, passport, **extra_fields)



class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    first_name = models.CharField(max_length=50, blank=False, null=False,help_text='Имя')
    last_name = models.CharField(max_length=50, blank=False, null=False,help_text='Фамилия')
    father_name = models.CharField(max_length=50, blank=True, null=True,help_text='Отчество')
    passport = EncryptedCharField()
    phone = PhoneNumberField(blank=False, null=False)
    email = models.EmailField("email address", unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, blank=True, null=True)

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Администратор'
        RULER = 'RULER', 'Руководитель'
        PROJECT_MANAGER = 'PROJECT_MANAGER', 'Менеджер проекта'
        STAGE_MANAGER = 'STAGE_MANAGER', 'Менеджер этапа'
        DUMMY = 'DUMMY', 'Пользователь без прав'

    role = models.CharField(max_length=25, choices=Role.choices, default=Role.DUMMY)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "passport", "phone"]

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
