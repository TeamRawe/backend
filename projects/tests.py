from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from users.models import User
from contractors.models import SubContractor, GovernmentalCompany
from .models import Project, Stage, File, ProjectAssignment, StageAssignment, StageReport, ProjectReport

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.customer = GovernmentalCompany.objects.create(name="Test Customer")
        self.project = Project.objects.create(
            title="Test Project",
            description="Project Description",
            start_date=now().date(),
            end_date=(now() + timedelta(days=10)).date(),
            planned_cost=10000.00,
            customer=self.customer,
            created_by=self.user
        )

    def test_project_dates_validation(self):
        self.project.end_date = self.project.start_date - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.project.clean()

    def test_project_progress_validation(self):
        self.project.progress = 110
        with self.assertRaises(ValidationError):
            self.project.clean()

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")


class StageModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.customer = GovernmentalCompany.objects.create(name="Test Customer")
        self.project = Project.objects.create(
            title="Test Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=30)).date(),
            planned_cost=10000.00,
            customer=self.customer,
            created_by=self.user
        )
        self.subcontractor = SubContractor.objects.create(name="Test Contractor")

    def test_stage_dates_validation(self):
        stage = Stage(
            project=self.project,
            title="Test Stage",
            start_date=self.project.start_date - timedelta(days=5),
            end_date=self.project.start_date - timedelta(days=1),
            planned_cost=5000.00,
            worker=self.subcontractor
        )
        with self.assertRaises(ValidationError):
            stage.clean()

    def test_stage_budget_exceeds_project(self):
        stage = Stage(
            project=self.project,
            title="Test Stage",
            start_date=self.project.start_date,
            end_date=self.project.end_date,
            planned_cost=15000.00,
            worker=self.subcontractor
        )
        with self.assertRaises(ValidationError):
            stage.clean()

    def test_stage_str(self):
        stage = Stage.objects.create(
            project=self.project,
            title="Test Stage",
            start_date=self.project.start_date,
            end_date=self.project.end_date,
            planned_cost=5000.00,
            worker=self.subcontractor
        )
        self.assertEqual(str(stage), f'{stage.number} {stage.title}')


class FileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.project = Project.objects.create(
            title="Test Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=30)).date(),
            planned_cost=10000.00,
            created_by=self.user
        )

    def test_file_category_auto_assignment(self):
        file = File.objects.create(
            project=self.project,
            created_by=self.user,
            file="test.doc"
        )
        file.save()
        self.assertEqual(file.category, File.FileCategory.DOCUMENT)

    def test_file_must_have_project_or_stage(self):
        file = File(created_by=self.user)
        with self.assertRaises(ValidationError):
            file.clean()

    def test_file_str(self):
        file = File.objects.create(
            project=self.project,
            created_by=self.user,
            file="test.pdf",
            category=File.FileCategory.DOCUMENT
        )
        self.assertEqual(str(file), "DOCUMENT - test.pdf")


class ProjectAssignmentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.project = Project.objects.create(
            title="Test Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=30)).date(),
            planned_cost=10000.00,
            created_by=self.user
        )

    def test_project_assignment_dates_validation(self):
        assignment = ProjectAssignment(
            target=self.project,
            user=self.user,
            activate_at=now(),
            deactivate_at=now() - timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            assignment.clean()


class StageReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.project = Project.objects.create(
            title="Test Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=30)).date(),
            planned_cost=10000.00,
            created_by=self.user
        )
        self.stage = Stage.objects.create(
            project=self.project,
            title="Test Stage",
            start_date=self.project.start_date,
            end_date=self.project.end_date,
            planned_cost=5000.00,
            worker=None
        )

    def test_stage_report_must_be_linked_to_stage(self):
        report = StageReport(title="Test Report", created_by=self.user)
        with self.assertRaises(ValidationError):
            report.clean()

    def test_stage_report_status_change(self):
        report = StageReport.objects.create(
            stage=self.stage,
            title="Test Report",
            created_by=self.user,
            status="PENDING"
        )
        report.status = "APPROVED"
        report.save()
        self.assertEqual(report.status, "APPROVED")
