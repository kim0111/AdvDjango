from celery import shared_task
from resumes.models import Resume
from core_ai.nlp import parse_resume_text


@shared_task
def analyze_resume(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        result = parse_resume_text(resume.extracted_text)
        resume.skills = result['skills']
        resume.experience = result['experience']
        resume.education = result['education']
        resume.save()
        return f"Resume {resume_id} analyzed successfully"
    except Exception as e:
        return str(e)
