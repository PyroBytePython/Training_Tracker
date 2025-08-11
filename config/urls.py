from django.contrib import admin
from django.urls import path, include

from Tracker.views import HomeView
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='root'),  # главная страница
    path('admin/', admin.site.urls),
    path('tracker/', include('Tracker.urls', namespace='tracker')),
    path('users/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
