from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracker/', include('Tracker.urls', namespace='trackers')),
    path('users/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
