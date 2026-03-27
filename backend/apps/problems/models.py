from django.db import models

# Create your models here.
class Problems(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    difficulty = models.CharField(choices=Difficulty, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{Problems.title}"

class TestCase(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name = 'test_cases')
    input = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)