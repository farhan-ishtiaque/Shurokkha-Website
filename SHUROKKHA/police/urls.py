from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.police_login_view, name='police_login'),
    path('dashboard/', views.police_dashboard, name='police_dashboard'),
    path('change-password/', views.police_change_password, name='police_change_password'),  
]
