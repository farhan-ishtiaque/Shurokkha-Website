"""
URL configuration for SHUROKKHA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from Login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('police/', include('police.urls')),
    path('fire/', include('firestation.urls')),  # 👈 works like 'police/'

 
path('login/', views.custom_login, name='login'),

    # Optional: use built-in logout view or your own

    # Redirect user after login based on role
    path('redirect_user/', views.redirect_user, name='redirect_user'),

    # Include your app's URLs (for dashboard, operator management, etc.)
    path('', include('Login.urls')),
    

]