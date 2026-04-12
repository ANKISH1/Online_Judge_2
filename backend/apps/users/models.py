from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    avatar = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile" 
    
          