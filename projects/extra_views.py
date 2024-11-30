from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_project_file
import os
from users.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

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
    user = request.user
    assigned_projects = ProjectAssignment.objects.filter(user=user, status=ProjectAssignment.AssignmentStatus.ACTIVE)
    if not assigned_projects.filter(target_id=project_id).exists() and not (user.Role.ADMIN or user.Role.RULER):
        return Response({"error": "Prohibited"}, status=404)

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
    user = request.user
    assigned_stages = StageAssignment.objects.filter(user=user, status=StageAssignment.AssignmentStatus.ACTIVE)
    if not assigned_stages.filter(target_id=stage_id).exists() and not (user.Role.ADMIN or user.Role.RULER):
        return Response({"error": "Prohibited"}, status=404)

    try:
        stage = Stage.objects.get(id=stage_id)

        substages = stage.children_stages.all()

        serializer = ReadStageSerializer(substages, many=True)

        return Response(serializer.data)

    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_files(request, project_id, type=""):
    user = request.user
    assigned_projects = ProjectAssignment.objects.filter(user=user, status=ProjectAssignment.AssignmentStatus.ACTIVE)
    if not assigned_projects.filter(target_id=project_id).exists() and not (user.Role.ADMIN or user.Role.RULER):
        return Response({"error": "Prohibited"}, status=404)
    try:
        project = Project.objects.get(id=project_id)

        if type == "":
            files = File.objects.filter(project=project)

            serializer = ReadFileSerializer(files, many=True)

            return Response(serializer.data)

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
def get_stage_files(request, stage_id, type=""):
    user = request.user
    assigned_stages = StageAssignment.objects.filter(user=user, status=StageAssignment.AssignmentStatus.ACTIVE)
    if not assigned_stages.filter(target_id=stage_id).exists() and not (user.Role.ADMIN or user.Role.RULER):
        return Response({"error": "Prohibited"}, status=404)
    try:
        stage = Stage.objects.get(id=stage_id)

        if type == "":
            files = File.objects.filter(stage=stage)

            serializer = ReadFileSerializer(files, many=True)

            return Response(serializer.data)

        if type not in [category[0] for category in File.FileCategory.choices]:
            return Response({"error": "Invalid file category type"}, status=400)

        files = File.objects.filter(stage=stage, category=type)

        serializer = ReadFileSerializer(files, many=True)

        return Response(serializer.data)

    except Project.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    try:
        # Получаем файл по id из базы данных
        uploaded_file = File.objects.get(id=file_id)

        # Путь к файлу на сервере
        file_path = uploaded_file.file.path

        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(uploaded_file.file.name)}"'

        return response

    except File.DoesNotExist:
        raise Http404("File not found")

@permission_classes([IsAuthenticated])
class FileUploaderView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = CreateFileSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            return Response({
                "id": file_instance.id,
            }, status=status.HTTP_201_CREATED)
        else:
            logger.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required_fbv(['ADMIN'])
def make_ms_project(request):
    # Проверяем, что файл передан
    if 'file' not in request.FILES:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    file_path = os.path.join('uploaded_projects', file.name)

    # Сохраняем файл
    try:
        # Сохраняем файл на сервере
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Запускаем задачу Celery для обработки этого файла
        process_project_file.apply_async(args=[file_path])

        return Response({"status": "success", "message": "Project file is being processed."},
                        status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_data(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        stages = project.stages.all()
        project_serializer = ReadProjectSerializer(project)
        stage_serializer = ReadStageSerializer(stages, many=True)

        return Response({
            "project": project_serializer.data,
            "stages": stage_serializer.data
        })

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stage_data(request, stage_id):
    try:
        stage = Stage.objects.get(id=stage_id)
        substages = stage.children_stages.all()
        stage_serializer = ReadStageSerializer(stage)
        substage_serializer = ReadStageSerializer(substages, many=True)

        return Response({
            "stage": stage_serializer.data,
            "substages": substage_serializer.data
        })

    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stage_completion_percentage(request, stage_id):
    try:
        stage = Stage.objects.get(id=stage_id)
        substages = stage.children_stages.all()

        # Расчет процента выполнения для этапа
        stage_completion = stage.tasks.filter(status='COMPLETED').count()
        stage_total = stage.tasks.count()
        stage_percentage = (stage_completion / stage_total * 100) if stage_total > 0 else 0

        # Расчет процента выполнения для подэтапов
        substages_completion_data = []
        for substage in substages:
            substage_completion = substage.tasks.filter(status='COMPLETED').count()
            substage_total = substage.tasks.count()
            substage_percentage = (substage_completion / substage_total * 100) if substage_total > 0 else 0
            substages_completion_data.append({
                "substage_id": substage.id,
                "substage_name": substage.name,
                "completion_percentage": substage_percentage
            })

        return Response({
            "stage_id": stage.id,
            "stage_name": stage.name,
            "stage_completion_percentage": stage_percentage,
            "substages": substages_completion_data
        })

    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=404)