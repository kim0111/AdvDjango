# from rest_framework import viewsets, permissions
# from rest_framework.response import Response
# from .models import Resume
# from .serializers import ResumeSerializer
# from .utils import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
# from datetime import datetime
# from analytics.utils import log_event
# from resumes.tasks import analyze_resume
#
#
# class ResumeViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def list(self, request):
#         resumes = Resume.objects(user_id=request.user.id)
#         serializer = ResumeSerializer(resumes, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         file = request.FILES['original_file']
#         ext = file.name.split('.')[-1].lower()
#
#         if ext == 'pdf':
#             text = extract_text_from_pdf(file)
#         elif ext == 'docx':
#             text = extract_text_from_docx(file)
#         else:
#             log_event('ERROR', f'Unsupported resume file: {file.name}', user=request.user)
#             return Response({'error': 'Unsupported file type'}, status=400)
#
#         parsed = parse_resume_text(text)
#
#         resume = Resume(
#             user_id=request.user.id,
#             original_file_name=file.name,
#             extracted_text=text,
#             skills=parsed['skills'],
#             experience=parsed['experience'],
#             education=parsed['education'],
#             created_at=datetime.utcnow()
#         )
#         resume.save()
#         analyze_resume.delay(str(resume.id))
#
#         log_event('UPLOAD', f'Resume uploaded (mongoengine): {file.name}', user=request.user)
#
#         serializer = ResumeSerializer(resume)
#         return Response(serializer.data)
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .models import Resume
from datetime import datetime
import os
from .utils import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
from analytics.utils import log_event


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1].lower()

        filename = f"media/resumes/{file.name}"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        if ext == '.pdf':
            text = extract_text_from_pdf(filename)
        elif ext == '.docx':
            text = extract_text_from_docx(filename)
        else:
            text = 'Unsupported file type'

        parsed = parse_resume_text(text)
        combined_text = f"🧠 Skills: {parsed['skills']}\n\n📌 ⚙️Experience:\n{parsed['experience']}\n\n🎓 📖Education:\n{parsed['education']}"

        resume = Resume(
            user_id=request.user.id,
            file_path=filename,
            parsed_text=combined_text,
            created_at=datetime.utcnow()
        )
        resume.save()
        log_event('UPLOAD', f'Resume uploaded (mongoengine): {file.name}', user=request.user)
        return Response({"message": "Resume uploaded successfully", "id": str(resume.id)})


class ResumeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects(user_id=request.user.id)
        data = [
            {
                "id": str(r.id),
                "file_path": r.file_path,
                "parsed_text": r.parsed_text,
                "created_at": r.created_at
            } for r in resumes
        ]
        return Response(data)
