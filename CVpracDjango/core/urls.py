from django.urls import path

from .views import contact_view
from django.conf import settings

from django.conf.urls.static import static

# urlpatterns = [
#
#     path('contact/', contact_view, name='contact'),
#
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)