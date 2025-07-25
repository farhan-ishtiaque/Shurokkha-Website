# app_auth/urls.py

from django.urls import path
from .views import register_user
from .views import login_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
