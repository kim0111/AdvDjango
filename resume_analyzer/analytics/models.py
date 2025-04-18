from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LogEntry(models.Model):
    EVENT_CHOICES = [
        ('UPLOAD', 'Resume Uploaded'),
        ('MATCH', 'Job Matched'),
        ('ERROR', 'Error Occurred'),
        ('LOGIN', 'User Logged In'),
        ('REGISTER', 'User Registered'),
    ]

    user_id = models.IntegerField(null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "analytics_logs"
