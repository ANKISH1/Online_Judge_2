from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User
from apps.problems.models import Problems
from django.urls import reverse

# Create your tests here.
class SubmissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.all_submissions_url = reverse('all_submissions')
        self.problem_submission_url = reverse('problem_submission', kwargs={'pk': 1})
        self.user = User.objects.create_user(
            email = "test@test.com",
            username= "testuser",
            password = "testpassword"
        )
        self.problem= Problems.objects.create(
            title = "Merge arrays",
            description = "testdescription",
            difficulty = "HARD"
        )
        self.data = {
            "problem":1,
            "language":"python",
            "code":"print('Hello World')"
        }  

    def test_authenticated_user_can_create_submissions(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.post(self.problem_submission_url,self.data)
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_user_cannot_create_submissions(self):  
        self.client.force_authenticate(user = None)
        response = self.client.post(self.problem_submission_url,self.data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_view_submissions(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get(self.all_submissions_url)
        self.assertEqual(response.status_code, 200)    

    def test_unauthenticated_user_cannot_view_submissions(self):    
        self.client.force_authenticate(user = None)
        response = self.client.get(self.all_submissions_url)
        self.assertEqual(response.status_code, 401) 
        