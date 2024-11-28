from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_project_file
import os
from users.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *


@csrf_exempt
def project_from_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file part"}, status=400)

        uploaded_file = request.FILES['file']
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Запускаем задачу Celery
        task = process_project_file.delay(file_path)
        return JsonResponse({"task_id": task.id}, status=202)
    return JsonResponse({"error": "Invalid request"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_projects(request):
    user = request.user
    assigned_projects = ProjectAssignment.objects.filter(user=user, status=ProjectAssignment.AssignmentStatus.ACTIVE)
    projects = [assignment.target for assignment in assigned_projects]
    serializer = ReadProjectSerializer(projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_stages(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

        stages = project.stages.all()

        serializer = ReadStageSerializer(stages, many=True)

        return Response(serializer.data)

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stage_substages(request, stage_id):
    try:
        stage = Stage.objects.get(id=stage_id)

        substages = stage.children_stages.all()

        serializer = ReadStageSerializer(substages, many=True)

        return Response(serializer.data)

    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_files(request, project_id, type):
    try:
        project = Project.objects.get(id=project_id)

        # Проверяем, что переданный тип файла является допустимым
        if type not in [category[0] for category in File.FileCategory.choices]:
            return Response({"error": "Invalid file category type"}, status=400)

        files = File.objects.filter(project=project, category=type)

        serializer = ReadFileSerializer(files, many=True)

        return Response(serializer.data)

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stage_files(request, stage_id, type):
    try:
        stage = Stage.objects.get(id=stage_id)

        if type not in [category[0] for category in File.FileCategory.choices]:
            return Response({"error": "Invalid file category type"}, status=400)

        files = File.objects.filter(stage=stage, category=type)

        serializer = ReadFileSerializer(files, many=True)

        return Response(serializer.data)

    except Project.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)


