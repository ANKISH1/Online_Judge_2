from django.db import models
from apps.users.models import User
from apps.problems.models import Problems

# Create your models here.
class Submissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE, db_index=True)
    class Language(models.TextChoices):
        C = "c", "C"
        CPP = "cpp","C++"
        PYTHON = "python", "Python"  
    class Verdict(models.TextChoices):
        ACCEPTED  = "ACCEPTED", "Accepted"
        WRONG_ANSWER = "WRONG_ANSWER", "Wrong Answer"
        TLE= "TLE", "Time Limit Exceeded"
        RE = "RE", "Runtime Error"
        CE = "CE", "Compilation Error"
        PENDING = "PENDING", "Pending"

    code = models.TextField(max_length=500)
    language = models.CharField(choices=Language.choices, max_length=10, )
    verdict = models.CharField(choices=Verdict, max_length=20, default="PENDING")
    submitted = models.DateTimeField(auto_now_add=True)        