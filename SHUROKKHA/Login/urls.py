from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
router = DefaultRouter() #registering default api routes from view set
router.register(r'tasks', TaskViewSet)
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'), #refreshes access token
    path('api/', include(router.urls)),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('operator_dashboard/', views.operator_dashboard, name='operator_dashboard'),
    path('operators/', views.operator_list, name='operator_list'),
    path('operators/add/', views.add_operator, name='add_operator'),
    path('operators/edit/<int:user_id>/', views.edit_operator, name='edit_operator'),
    path('operators/delete/<int:user_id>/', views.delete_operator, name='delete_operator'),
    path('operators/set_password/<int:user_id>/', views.set_password, name='set_operator_password'),
    path('search/', views.search_list, name='search_list'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),



    

  
]
