from rest_framework import serializers
from .models import *
from users.models import User  # Ensure User model import

class ReadFileSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # Only for read

    class Meta:
        model = File
        fields = ['id', 'project', 'stage', 'category', 'file', 'created_by']
        read_only_fields = ['id', 'category', 'created_by']


class CreateFileSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set to current user

    class Meta:
        model = File
        fields = ['project', 'stage', 'file', 'created_by']
        read_only_fields = ['category']  # Category will be automatically set in the model's save method

    def validate(self, data):
        # Validation to ensure file is linked to either project or stage
        if not data.get('project') and not data.get('stage'):
            raise serializers.ValidationError("File must be linked to either a project or a stage.")
        return data


class ReadProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only field

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'planned_cost', 'customer', 'progress', 'created_by']
        read_only_fields = ['id', 'created_by']


class CreateProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set to current user

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'planned_cost', 'customer', 'status', 'progress', 'created_by']


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'planned_cost', 'customer', 'status', 'progress']


class ProjectAssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only field

    class Meta:
        model = ProjectAssignment
        fields = ['id', 'user', 'target', 'activate_at', 'deactivate_at', 'status', 'created_by']
        read_only_fields = ['id', 'created_by']


class StageAssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only field

    class Meta:
        model = StageAssignment
        fields = ['id', 'user', 'target', 'activate_at', 'deactivate_at', 'status', 'created_by']
        read_only_fields = ['id', 'created_by']


class ReadStageSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only field

    class Meta:
        model = Stage
        fields = ['id', 'project', 'parent_stage', 'title', 'start_date', 'end_date', 'planned_cost', 'status', 'number', 'progress', 'created_by']
        read_only_fields = ['id', 'number', 'created_by']


class CreateStageSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set to current user

    class Meta:
        model = Stage
        fields = ['project', 'parent_stage', 'title', 'start_date', 'end_date', 'planned_cost', 'status', 'progress', 'created_by']


class UpdateStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['title', 'start_date', 'end_date', 'planned_cost', 'status', 'progress']


class StageReportSerializer(serializers.ModelSerializer):
    files = ReadFileSerializer(many=True, read_only=True)  # Nested serializer for files

    class Meta:
        model = StageReport
        fields = ['id', 'title', 'commentary', 'created_at', 'stage', 'files', 'created_by']

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        stage_report = StageReport.objects.create(**validated_data)
        stage_report.files.set(files_data)  # Link files to the report
        return stage_report


class ProjectReportSerializer(serializers.ModelSerializer):
    files = ReadFileSerializer(many=True, read_only=True)  # Nested serializer for files

    class Meta:
        model = ProjectReport
        fields = ['id', 'title', 'commentary', 'created_at', 'project', 'files', 'created_by']

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        project_report = ProjectReport.objects.create(**validated_data)
        project_report.files.set(files_data)  # Link files to the report
        return project_report


class StageReportCreateSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False,
                                      allow_null=True)  # Необязательное поле для бюджета

    class Meta:
        model = StageReport
        fields = ['title', 'commentary', 'stage', 'files', 'budget']

    def validate_budget(self, value):
        """
        Проверка, что бюджет не превышает бюджет связанного этапа.
        """
        if value is not None:
            stage_instance = self.initial_data.get('stage')
            stage = Stage.objects.get(id=stage_instance)  # Получаем экземпляр Stage по ID
            if value > stage.budget:
                raise serializers.ValidationError(f"Бюджет не может превышать бюджет этапа ({stage.budget}).")
        return value

    def create(self, validated_data):
        """
        Создание нового отчета.
        """
        files_data = validated_data.pop('files', [])
        # Устанавливаем статус по умолчанию
        validated_data['status'] = 'PENDING'

        # Создаем StageReport
        stage_report = StageReport.objects.create(**validated_data)

        # Привязываем файлы к отчету
        stage_report.files.set(files_data)

        # Возвращаем созданный объект
        return stage_report


class ProjectCreateSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'stage', 'files', 'status']

    def validate_status(self, value):
        """
        Если статус не был передан, то установим его как 'PENDING' (по умолчанию).
        """
        if not value:
            value = 'PENDING'
        return value

    def create(self, validated_data):
        """
        Создание нового проекта с установкой статуса по умолчанию.
        """
        files_data = validated_data.pop('files', [])

        # Устанавливаем статус по умолчанию, если не был передан
        validated_data['status'] = validated_data.get('status', 'PENDING')

        # Создаем проект
        project = Project.objects.create(**validated_data)

        # Привязываем файлы к проекту
        project.files.set(files_data)

        # Возвращаем созданный объект проекта
        return project
