from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    experience_required = models.PositiveIntegerField()
    skills_required = models.JSONField(default=list)  # List of skills
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
