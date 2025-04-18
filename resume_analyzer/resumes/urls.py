from django.urls import path
from .views import ResumeUploadView, ResumeListView

urlpatterns = [
    path('resumes/', ResumeListView.as_view(), name='resume-list'),
    path('resumes/upload/', ResumeUploadView.as_view(), name='resume-upload'),
]