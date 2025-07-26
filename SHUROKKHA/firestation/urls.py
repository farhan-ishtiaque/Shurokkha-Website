from django.urls import path
from . import views

urlpatterns = [
   
path('login/', views.fire_login_view, name='fire_login'),
    path('dashboard/', views.fire_dashboard, name='fire_dashboard'),
    path('change-password/', views.fire_change_password, name='fire_change_password'),
]