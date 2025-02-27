from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .models import AnalyticsReport
from .tasks import generate_trading_report, generate_profit_loss_report


class GenerateTradingReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = generate_trading_report.delay(request.user.id)
        return Response({"message": "Trading report generation started!", "task_id": task.id})


class GenerateProfitLossReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = generate_profit_loss_report.delay(request.user.id)
        return Response({"message": "Profit/Loss report generation started!", "task_id": task.id})


class DownloadReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_id):
        report = AnalyticsReport.objects.filter(id=report_id, generated_by=request.user).first()
        if not report:
            return Response({"error": "Report not found"}, status=404)
        return FileResponse(open(report.file.path, 'rb'), as_attachment=True)