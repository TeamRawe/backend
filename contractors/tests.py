from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from users.models import User
from contractors.models import GovernmentalCompany
from projects.models import Project


class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.customer = GovernmentalCompany.objects.create(name="Test Customer")

    def test_project_end_date_before_start_date(self):
        project = Project(
            title="Invalid Project",
            start_date=now().date(),
            end_date=(now() - timedelta(days=1)).date(),
            planned_cost=5000.00,
            customer=self.customer,
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            project.clean()

    def test_project_progress_exceeding_100(self):
        project = Project(
            title="Invalid Progress",
            start_date=now().date(),
            end_date=(now() + timedelta(days=10)).date(),
            planned_cost=5000.00,
            customer=self.customer,
            created_by=self.user,
            progress=110
        )
        with self.assertRaises(ValidationError):
            project.clean()

    def test_unique_project_title(self):
        Project.objects.create(
            title="Unique Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=10)).date(),
            planned_cost=5000.00,
            customer=self.customer,
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            duplicate_project = Project(
                title="Unique Project",
                start_date=now().date(),
                end_date=(now() + timedelta(days=10)).date(),
                planned_cost=5000.00,
                customer=self.customer,
                created_by=self.user
            )
            duplicate_project.full_clean()

    def test_project_str_representation(self):
        project = Project.objects.create(
            title="Test Project",
            start_date=now().date(),
            end_date=(now() + timedelta(days=10)).date(),
            planned_cost=5000.00,
            customer=self.customer,
            created_by=self.user
        )
        self.assertEqual(str(project), "Test Project")
