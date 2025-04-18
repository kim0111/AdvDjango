from rest_framework import viewsets, permissions
from .models import LogEntry
from .serializers import LogEntrySerializer


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-timestamp')
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAdminUser]
