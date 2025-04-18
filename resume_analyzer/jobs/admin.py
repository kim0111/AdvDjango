from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'recruiter', 'location', 'experience_required', 'created_at')
    list_filter = ('company', 'location', 'experience_required')
    search_fields = ('title', 'description', 'company')
