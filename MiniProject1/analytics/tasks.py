import csv
import os
from celery import shared_task
from django.utils.timezone import now
from django.conf import settings
from .models import AnalyticsReport
from trading.models import Order
from reportlab.pdfgen import canvas


def get_report_file_path(report_type, extension):
    file_name = f"{report_type}_report_{now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    file_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


@shared_task
def generate_trading_report(user_id):
    file_path = get_report_file_path('trading_report', 'csv')

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'User', 'Type', 'Price', 'Quantity', 'Status', 'Created At'])
        for order in Order.objects.all():
            writer.writerow([order.id, order.user.username, order.order_type, order.price, order.quantity, order.status,
                             order.created_at])

    AnalyticsReport.objects.create(
        user_id=user_id,
        report_type='trading_report',
        data={'file_path': file_path}
    )

    return f"Trading report generated: {file_path}"


@shared_task
def generate_profit_loss_report(user_id):
    file_path = get_report_file_path('profit_loss', 'pdf')

    c = canvas.Canvas(file_path)
    c.drawString(100, 800, "Profit/Loss Report")

    total_revenue = sum(order.price * order.quantity for order in Order.objects.all())
    total_cost = sum(order.quantity * order.price * 0.7 for order in Order.objects.all())  # Assuming cost is 70%
    profit_loss = total_revenue - total_cost

    c.drawString(100, 770, f"Total Revenue: {total_revenue}")
    c.drawString(100, 750, f"Total Cost: {total_cost}")
    c.drawString(100, 730, f"Profit/Loss: {profit_loss}")

    c.save()

    AnalyticsReport.objects.create(
        user_id=user_id,
        report_type='profit_loss',
        data={'file_path': file_path, 'total_revenue': total_revenue, 'total_cost': total_cost,
              'profit_loss': profit_loss}
    )

    return f"Profit/Loss report generated: {file_path}"
