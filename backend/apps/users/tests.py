from django.test import TestCase
from rest_framework.test import APIClient 
from .models import User
from django.urls import reverse
# Create your tests here.

class UserAuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.data = {
            "email":"test@test.com",
            "username":"TestUser",
            "password":"testpassword"
        }


    def test_register_creates_user(self):
        response = self.client.post(self.register_url,self.data)

        self.assertEqual(response.status_code,201)    
        self.assertTrue(User.objects.filter(email = "test@test.com").exists())

    def test_register_duplicate_email(self):
        response1 = self.client.post(self.register_url, self.data)
        self.assertEqual(response1.status_code,201)   

        response2 = self.client.post(self.register_url, self.data)
        self.assertEqual(response2.status_code,400 )       

    def test_login_success(self):
        self.client.post(self.register_url,self.data)
        response = self.client.post(self.login_url, self.data)
        self.assertEqual(response.status_code,200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_login_wrong_password(self):
        self.client.post(self.register_url,self.data)
        data2 =  {
            "email":"test@test.com",
            "username":"TestUser",
            "password":"thisiswrongpassword"
        }
        response = self.client.post(self.login_url,data2)  
        self.assertEqual(response.status_code, 400)      