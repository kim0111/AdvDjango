from django.db import models
from django.contrib.auth import get_user_model


class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('trading_report', 'Trading Report'),
        ('profit_loss', 'Profit/Loss'),
        ('revenue_tracking', 'Revenue Tracking')
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return f"{self.get_report_type_display()} Report - {self.generated_at}"
