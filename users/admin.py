from django.contrib import admin
from .models import User  # Импорт модели User
from django import forms
from django.core.exceptions import ValidationError
class UserChangeForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=(
            "Пароль будет автоматически хэширован при сохранении."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.instance.pk and not password:  # При создании проверяем, что пароль задан
            raise ValidationError("Пароль является обязательным при создании пользователя.")
        return password

class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ('first_name', 'father_name','last_name', 'email', 'role', 'phone')  # Поля для отображения в списке
    search_fields = ('phone', 'last_name', 'email', 'role')  # Поля для поиска
    list_filter = ('role',)  # Фильтр по ролям
    ordering = ('last_name', 'first_name')  # Сортировка по фамилии и имени

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'father_name', 'email', 'passport', 'phone', 'role','password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser')
        }),
    )

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get("password")
        if password:
            obj.set_password(password)  # Хэшируем и сохраняем пароль
        super().save_model(request, obj, form, change)

# Регистрация модели User с кастомным UserAdmin
admin.site.register(User, UserAdmin)