from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.timezone import now


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123"
        )
        self.admin_user = User.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="adminpassword"
        )
        self.admin_user.role = "ADMIN"
        self.admin_user.save()

    # Tests for login_view
    def test_login_successful(self):
        response = self.client.post('/api/login/', {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    # Tests for logout_view
    def test_logout_successful(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_logout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests for test
    def test_csrf_token_generation(self):
        response = self.client.get('/api/test/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('csrftoken', response.cookies)

    # Tests for secure_test
    def test_secure_test_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/secure-test/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_secure_test_unauthenticated(self):
        response = self.client.get('/api/secure-test/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests for test_role
    def test_access_with_valid_role(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/test-role/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_access_with_invalid_role(self):
        self.user.role = "USER"
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/test-role/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Tests for check_session
    def test_valid_session(self):
        self.client.force_login(self.user)
        session = self.client.session
        session.set_expiry(300)
        session.save()
        response = self.client.get(
            '/api/check-session/',
            HTTP_COOKIE=f'sessionid={self.client.cookies["sessionid"].value}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_invalid_session(self):
        response = self.client.get('/api/check-session/')
        self.assertEqual(response.status_code, 400)

    # Tests for UserViewSet
    def test_create_user_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'USER'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_by_self(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

    def test_update_user_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f'/api/users/{self.user.id}/', {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_not_allowed(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
