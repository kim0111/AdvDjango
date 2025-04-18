# Generated by Django 3.1.12 on 2025-04-08 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('UPLOAD', 'Resume Uploaded'), ('MATCH', 'Job Matched'), ('ERROR', 'Error Occurred'), ('LOGIN', 'User Logged In'), ('REGISTER', 'User Registered')], max_length=20)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytics_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'analytics_logs',
            },
        ),
    ]
