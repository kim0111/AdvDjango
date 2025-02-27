from django.urls import path
from .views import GenerateTradingReportView, GenerateProfitLossReportView, DownloadReportView

urlpatterns = [
    path('trading-report/', GenerateTradingReportView.as_view(), name='generate_trading_report'),
    path('profit-loss-report/', GenerateProfitLossReportView.as_view(), name='generate_profit_loss_report'),
    path('download/<int:report_id>/', DownloadReportView.as_view(), name='download_report'),
]