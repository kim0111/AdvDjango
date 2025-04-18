from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    compatibility_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company', 'location',
            'experience_required', 'skills_required', 'recruiter',
            'is_active', 'created_at', 'compatibility_score'
        ]
        read_only_fields = ['recruiter', 'created_at', 'compatibility_score']
