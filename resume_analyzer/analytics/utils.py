# analytics/utils.py
from analytics.models import LogEntry
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


def log_event(event_type: str, message: str, user=None):
    """
    Centralized log writer to MySQL database via analytics.LogEntry.

    Args:
        event_type (str): One of ('UPLOAD', 'MATCH', 'ERROR', 'LOGIN', 'REGISTER')
        message (str): Description of the event
        user (User): Optional user instance
    """
    try:
        LogEntry.objects.using('mysql').create(
            user_id=user.id if user else None,
            event_type=event_type,
            message=message,
            timestamp=now()
        )
    except Exception as e:
        # Fallback to console logging or file (optional)
        print(f"[LOGGING ERROR] {e} — while logging: {event_type} | {message}")
