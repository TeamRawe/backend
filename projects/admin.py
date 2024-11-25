from django.contrib import admin
from .models import Project, Stage, File, ProjectAssignment, StageAssignment
from django.utils.translation import gettext_lazy as _


# Админка для модели File
class FileAdmin(admin.ModelAdmin):
    list_display = ('category', 'file', 'project', 'stage', 'created_at')
    search_fields = ('file', 'category', 'project__title', 'stage__title')
    list_filter = ('category', 'project', 'stage')
    ordering = ('-created_at',)

    # Добавим возможность редактировать категорию и файл в одном окне
    fieldsets = (
        (None, {
            'fields': ('file', 'category', 'project', 'stage')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )


# Админка для модели Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'start_date', 'end_date', 'status', 'planned_cost')
    search_fields = ('title', 'customer__title', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date', 'customer')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'planned_cost', 'customer')
        }),
        (_('Dates'), {
            'fields': ('start_date', 'end_date'),
        }),
    )

class StageAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'start_date', 'end_date', 'status', 'planned_cost', 'project')
    search_fields = ('number', 'title', 'project__title', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date', 'project')
    ordering = ('number',)

    fieldsets = (
        (None, {
            'fields': ('number', 'title', 'start_date', 'end_date', 'status', 'planned_cost', 'project', 'parent_stage')
        }),
        # Удалили повторение 'planned_cost'
        # (_('Financial'), {
        #     'fields': ('planned_cost',),
        # }),
        # Удалили повторение 'status'
        # (_('Status'), {
        #     'fields': ('status',),
        # }),
    )



# Админка для модели ProjectAssignment
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'status', 'activate_at', 'deactivate_at')
    search_fields = ('user__username', 'target__title', 'status')
    list_filter = ('status', 'target', 'user')
    ordering = ('-activate_at',)


# Админка для модели StageAssignment
class StageAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'status', 'activate_at', 'deactivate_at')
    search_fields = ('user__username', 'target__title', 'status')
    list_filter = ('status', 'target', 'user')
    ordering = ('-activate_at',)


# Регистрируем модели в админке
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)
admin.site.register(StageAssignment, StageAssignmentAdmin)