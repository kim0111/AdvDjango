from rest_framework import viewsets, permissions
from .models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiter


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).order_by('-created_at')

        skills = self.request.query_params.getlist('skills')
        location = self.request.query_params.get('location')
        min_exp = self.request.query_params.get('min_experience')

        if skills:
            for skill in skills:
                queryset = queryset.filter(skills_required__icontains=skill)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if min_exp:
            queryset = queryset.filter(experience_required__gte=min_exp)

        # optional: compatibility_score можно подсчитать позже
        for job in queryset:
            job.compatibility_score = 0.0

        return queryset

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return super().get_permissions()
