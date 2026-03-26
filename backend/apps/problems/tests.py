from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User
from django.urls import reverse
from .models import Problems
# Create your tests here.

class ProblemCreateList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.all_problems_url = reverse('problems')
        self.user = User.objects.create_user(
            email="user@test.com",
            username="testuser",
            password="testpassword"
        )
        self.admin = User.objects.create_superuser(
            email="amdin@test.com",
            username="adminuser",
            password="adminpassword"
        )
        self.client.force_authenticate(user = self.user)
        self.data = {
            "title":"Merge Two Arrays",
            "description": "Merge two arrays",
            "difficulty":"EASY"

        }

    def test_admin_problem_create(self):
        self.client.force_authenticate(user = self.admin)
        response = self.client.post(self.all_problems_url, self.data)
        id = response.data['id']
        self.assertTrue(Problems.objects.filter(id = id).exists())
        self.assertEqual(response.status_code,201 )


    def test_user_problem_cannot_create(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.post(self.all_problems_url, self.data)
        self.assertEqual(response.status_code,403 )

    def test_authenticated_user_problems_list(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get(self.all_problems_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_problems_list(self):
        self.client.force_authenticate(user = None)
        response = self.client.get(self.all_problems_url)
        self.assertEqual(response.status_code, 401)