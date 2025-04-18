
from django import views
from django.contrib import admin
from Admins import views
from Clients import views
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name="home"),
    path('index.',include('Admins.urls')),
    path('index.',include('Clients.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
