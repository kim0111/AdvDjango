from django.contrib import admin
from .models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user_id', 'short_message', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    readonly_fields = ('event_type', 'user_id', 'message', 'timestamp')
    search_fields = ('message', 'event_type', 'user_id')
    ordering = ('-timestamp',)

    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message

    short_message.short_description = 'Message'
