from django.test import TestCase

# Create your tests here.

from contractors.models import *
from phonenumber_field.modelfields import PhoneNumberField


class ContactFaceTest(TestCase):
    def setUp(self):
        # Создаем объект ContactFace
        self.contact = ContactFace.objects.create(
            name="John Doe",
            phone="+1234567890",
            email="johndoe@example.com"
        )

    def test_contact_face_creation(self):
        # Проверяем, что объект был создан
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.phone, "+1234567890")
        self.assertEqual(self.contact.email, "johndoe@example.com")

    def test_contact_face_str_method(self):
        # Проверяем метод __str__
        self.assertEqual(str(self.contact), "John Doe")


class SubContractorTest(TestCase):

    def setUp(self):
        # Создаем объекты ContactFace
        self.contact1 = ContactFace.objects.create(name="John Doe")
        self.contact2 = ContactFace.objects.create(name="Jane Smith")

        # Создаем объект SubContractor
        self.sub_contractor = SubContractor.objects.create(
            title="Sub Contractor Ltd",
            inn="123456789012",
            ogrn="1234567890123",
            phone="+1122334455",
            email="subcontractor@example.com"
        )

    def test_sub_contractor_creation(self):
        # Проверяем, что субподрядчик был создан
        self.assertEqual(self.sub_contractor.title, "Sub Contractor Ltd")
        self.assertEqual(self.sub_contractor.inn, "123456789012")

    def test_many_to_many_relation(self):
        # Связываем контактные лица с субподрядчиком
        self.sub_contractor.contacts.add(self.contact1, self.contact2)

        # Проверяем, что контакты правильно добавлены
        self.assertEqual(self.sub_contractor.contacts.count(), 2)
        self.assertIn(self.contact1, self.sub_contractor.contacts.all())
        self.assertIn(self.contact2, self.sub_contractor.contacts.all())

class GovernmentalCompanyModelTest(TestCase):

    def setUp(self):
        self.gov_company = GovernmentalCompany.objects.create(
            title="Governmental Organization",
            address="123 Government Street",
            inn="987654321098",
            ogrn="9876543210987",
            phone="+1222333444",
            email="govorg@example.com"
        )

    def test_governmental_company_creation(self):
        # Проверка, что государственная компания была создана
        self.assertEqual(self.gov_company.title, "Governmental Organization")
        self.assertEqual(self.gov_company.inn, "987654321098")
        self.assertEqual(self.gov_company.ogrn, "9876543210987")
        self.assertEqual(self.gov_company.phone, "+1222333444")
        self.assertEqual(self.gov_company.email, "govorg@example.com")

    def test_governmental_company_str(self):
        # Проверка, что метод __str__ возвращает название компании
        self.assertEqual(str(self.gov_company), "Governmental Organization")