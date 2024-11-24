from rest_framework import serializers
from .models import *

class ReadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description','start_date',
                  'end_date','planned_cost', 'customer']

        read_only_fields = ['id']

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date',
                  'end_date', 'planned_cost', 'customer', 'status']

class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date',
                  'end_date', 'planned_cost', 'customer', 'status']

class ReadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'project', 'stage', 'category', 'file']
        read_only_fields = ['id', 'category']

class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['project', 'stage', 'file']

    def validate(self, data):
        # Проверка, что файл привязан либо к проекту, либо к этапу
        if not data.get('project') and not data.get('stage'):
            raise serializers.ValidationError("Файл должен быть связан либо с проектом, либо с этапом.")
        return data

class ProjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssignment
        fields = ['id', 'user', 'target', 'activate_at', 'deactivate_at', 'status']
        read_only_fields = ['id']

class StageAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageAssignment
        fields = ['id', 'user', 'target', 'activate_at', 'deactivate_at', 'status']
        read_only_fields = ['id']

class ReadStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'project', 'parent_stage', 'title', 'start_date', 'end_date', 'planned_cost', 'status', 'number']
        read_only_fields = ['id', 'number']

class CreateStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['project', 'parent_stage', 'title', 'start_date', 'end_date', 'planned_cost', 'status']

class UpdateStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['title', 'start_date', 'end_date', 'planned_cost', 'status']
