from django.contrib import admin
from .models import User  # Импорт модели User

# Если вы хотите кастомизировать отображение модели User в админке, создайте свой класс
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'phone')  # Поля для отображения в списке
    search_fields = ('first_name', 'last_name', 'email', 'role')  # Поля для поиска
    list_filter = ('role',)  # Фильтр по ролям
    ordering = ('last_name', 'first_name')  # Сортировка по фамилии и имени

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'father_name', 'email', 'passport', 'phone', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser')
        }),
    )

# Регистрация модели User с кастомным UserAdmin
admin.site.register(User, UserAdmin)