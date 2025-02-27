from celery import shared_task
from .models import Notification


def send_notification(user, message):
    Notification.objects.create(user=user, message=message)


@shared_task
def async_send_notification(user_id, message):
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
    user = user_model.objects.get(id=user_id)
    send_notification(user, message)
