# Generated by Django 5.1.3 on 2024-11-14 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Администратор'), ('RULER', 'Руководитель'), ('PROJECT_MANAGER', 'Менеджер проекта'), ('STAGE_MANAGER', 'Менеджер этапа'), ('DUMMY', 'Пользователь без прав')], default='DUMMY', max_length=25),
        ),
    ]
