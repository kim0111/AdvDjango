# from django.contrib import admin
# from mongoengine import Document
# from django.utils.html import format_html
# from resumes.models import Resume
#
#
# class ResumeAdmin(admin.ModelAdmin):
#     readonly_fields = ('preview_text',)
#
#     def preview_text(self, obj):
#         return format_html('<div style="max-height:200px;overflow:auto;">{}</div>', obj.extracted_text[:1000])
#


# from django.contrib import admin
# from .models import Resume
#
#
# @admin.register(Resume)
# class ResumeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'file', 'created_at')
#     search_fields = ('user__username',)
#     list_filter = ('created_at',)
