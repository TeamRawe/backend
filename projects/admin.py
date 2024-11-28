from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _


# Админка для модели File
class FileAdmin(admin.ModelAdmin):
    list_display = ('category', 'file', 'project', 'stage', 'created_at', 'created_by')
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
    list_display = ('title', 'customer','progress','created_by', 'start_date', 'end_date', 'status', 'planned_cost')
    search_fields = ('title', 'customer__title', 'start_date', 'end_date', 'status','created_by')
    list_filter = ('status', 'start_date', 'end_date', 'customer', 'created_by')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description','progress', 'status', 'planned_cost', 'customer')
        }),
        (_('Сроки'), {
            'fields': ('start_date', 'end_date'),
        }),
    )

class StageAdmin(admin.ModelAdmin):
    list_display = ('title','number','worker','progress', 'created_by', 'start_date', 'end_date', 'status', 'planned_cost', 'project')
    search_fields = ('number', 'title', 'project__title', 'start_date', 'end_date', 'created_by')
    list_filter = ('status', 'start_date', 'end_date', 'project', 'created_by')
    ordering = ('number', 'start_date')

    fieldsets = (
        (None, {
            'fields': ('title','progress', 'start_date', 'end_date', 'status', 'planned_cost', 'project', 'parent_stage','worker')
        }),
    )



# Админка для модели ProjectAssignment
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'status', 'activate_at', 'deactivate_at', 'created_by' )
    search_fields = ('user__username', 'target__title', 'status', 'created_by')
    list_filter = ('status', 'target', 'user', 'created_by')
    ordering = ('-activate_at',)
    readonly_fields = ('created_by',)


# Админка для модели StageAssignment
class StageAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'status', 'activate_at', 'deactivate_at', 'created_by')
    search_fields = ('user__username', 'target__title', 'status', 'created_by')
    list_filter = ('status', 'target', 'user', 'created_by')
    ordering = ('-activate_at',)
    readonly_fields = ('created_by',)


class StageReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'created_by', 'created_at','status',)
    list_filter = ('created_at', 'stage', 'created_by')
    search_fields = ('title', 'stage__name', 'created_by__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('files',)
    fieldsets = (
        (None, {
            'fields': ('title', 'commentary','status', 'stage', 'files', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'created_at','status',)
    list_filter = ('created_at', 'project', 'created_by')
    search_fields = ('title', 'project__name', 'created_by__username')
    readonly_fields = ('created_at','created_by')
    filter_horizontal = ('files',)
    fieldsets = (
        (None, {
            'fields': ('title', 'commentary', 'project', 'status', 'files', 'created_by')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
# Регистрируем модели в админке
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)
admin.site.register(StageAssignment, StageAssignmentAdmin)
admin.site.register(StageReport, StageReportAdmin)
admin.site.register(ProjectReport, ProjectReportAdmin)
