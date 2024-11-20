from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Project, Stage, File, ProjectAssignment, StageAssignment
from users.models import User
from contractors.models import GovernmentalCompany
from datetime import date, timedelta


class ProjectModelTest(TestCase):
    def setUp(self):
        self.company = GovernmentalCompany.objects.create(title="Test Company")
        self.project = Project.objects.create(
            title="Test Project",
            description="Description for Test Project",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            planned_cost=10000.00,
            customer=self.company
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.status, Project.ProjectStatus.PLANNED)

    def test_project_end_date_before_start_date(self):
        self.project.end_date = self.project.start_date - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.project.clean()

    def test_project_planned_cost_negative(self):
        self.project.planned_cost = -100
        with self.assertRaises(ValidationError):
            self.project.clean()


class StageModelTest(TestCase):
    def setUp(self):
        self.company = GovernmentalCompany.objects.create(title="Test Company")
        self.project = Project.objects.create(
            title="Test Project",
            description="Description for Test Project",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            planned_cost=10000.00,
            customer=self.company
        )
        self.stage = Stage.objects.create(
            project=self.project,
            title="Stage 1",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=15),
            planned_cost=5000.00
        )

    def test_stage_creation(self):
        self.assertEqual(self.stage.title, "Stage 1")
        self.assertEqual(self.stage.number, "1")

    def test_stage_sub_stage_numbering(self):
        sub_stage = Stage.objects.create(
            project=self.project,
            parent_stage=self.stage,
            title="Sub-stage 1",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            planned_cost=2500.00
        )
        self.assertEqual(sub_stage.number, "1.1")

    def test_stage_end_date_before_start_date(self):
        self.stage.end_date = self.stage.start_date - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.stage.clean()

    def test_stage_planned_cost_negative(self):
        self.stage.planned_cost = -100
        with self.assertRaises(ValidationError):
            self.stage.clean()


class FileModelTest(TestCase):
    def setUp(self):
        self.company = GovernmentalCompany.objects.create(title="Test Company")
        self.project = Project.objects.create(
            title="Test Project",
            description="Description for Test Project",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            planned_cost=10000.00,
            customer=self.company
        )

    def test_file_category_assignment(self):
        file_instance = File.objects.create(
            project=self.project,
            file="test_image.jpg"
        )
        file_instance.category = file_instance.recognise_filetype(file_instance.file.name)
        file_instance.save()
        self.assertEqual(file_instance.category, File.FileCategory.IMAGE)

    def test_file_without_project_or_stage_raises_error(self):
        # Создание файла без указания проекта или этапа
        file_instance = File(project=None, stage=None)  # Указываем, что оба поля пустые

        # Проверка, что выбрасывается ValidationError
        with self.assertRaises(ValidationError):
            file_instance.clean()  # Вызов валидации модели


class AssignmentModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя, используя email как username
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            passport="1234567890"
        )

        # Создаем тестовую компанию
        self.company = GovernmentalCompany.objects.create(title="Test Company")

        # Создаем тестовый проект
        self.project = Project.objects.create(
            title="Test Project",
            description="Description for Test Project",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            planned_cost=10000.00,
            customer=self.company
        )

        # Создаем тестовый этап для проекта
        self.stage = Stage.objects.create(
            project=self.project,
            title="Stage 1",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=15),
            planned_cost=5000.00
        )

    def test_project_assignment_activation(self):
        # Создаем назначение на проект и активируем его
        assignment = ProjectAssignment.objects.create(
            user=self.user,
            target=self.project,
            activate_at=date.today(),
            deactivate_at=date.today() + timedelta(days=10),
            status=ProjectAssignment.AssignmentStatus.FREEZED
        )
        assignment.activate()
        self.assertEqual(assignment.status, ProjectAssignment.AssignmentStatus.ACTIVE)

    def test_stage_assignment_deactivation(self):
        # Создаем назначение на этап и деактивируем его
        assignment = StageAssignment.objects.create(
            user=self.user,
            target=self.stage,
            activate_at=date.today(),
            deactivate_at=date.today() + timedelta(days=10),
            status=StageAssignment.AssignmentStatus.ACTIVE
        )
        assignment.deactivate()
        self.assertEqual(assignment.status, StageAssignment.AssignmentStatus.INACTIVE)

    def test_assignment_activate_at_before_deactivate_at(self):
        # Проверка, что `activate_at` раньше `deactivate_at`
        assignment = ProjectAssignment(
            user=self.user,
            target=self.project,
            activate_at=date.today() + timedelta(days=5),
            deactivate_at=date.today()
        )
        with self.assertRaises(ValidationError):
            assignment.clean()
