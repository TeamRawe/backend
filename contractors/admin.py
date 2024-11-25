from django.contrib import admin
from .models import ContactFace, SubContractor, GovernmentalCompany

# Админка для модели ContactFace
class ContactFaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')
    ordering = ('name',)

# Админка для модели SubContractor
class SubContractorAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'ogrn', 'phone', 'email')
    search_fields = ('title', 'inn', 'ogrn', 'phone', 'email')
    list_filter = ('inn', 'ogrn', 'phone', 'email')  # Фильтры по ИНН и ОГРН
    ordering = ('title',)
    filter_horizontal = ('contacts',)  # Для поля ManyToManyField

# Админка для модели GovernmentalCompany
class GovernmentalCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'ogrn', 'phone', 'email', 'website')
    search_fields = ('title', 'inn', 'ogrn', 'phone', 'email', 'website')
    list_filter = ('inn', 'ogrn', 'phone', 'email')  # Фильтры по ИНН и ОГРН
    ordering = ('title',)
    filter_horizontal = ('contacts',)  # Для поля ManyToManyField

# Регистрируем модели в админке
admin.site.register(ContactFace, ContactFaceAdmin)
admin.site.register(SubContractor, SubContractorAdmin)
admin.site.register(GovernmentalCompany, GovernmentalCompanyAdmin)
