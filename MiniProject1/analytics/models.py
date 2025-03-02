from django.db import models
from django.conf import settings


class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('trading', 'Trading Report'),
        ('sales', 'Sales Report'),
        ('profit_loss', 'Profit/Loss Report'),
    ]

    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/', default='reports/default.pdf')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.created_at})"

