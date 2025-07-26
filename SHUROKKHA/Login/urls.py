from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import add_police_station,police_station_list,TaskViewSet,fire_station_list,add_fire_station
router = DefaultRouter() #registering default api routes from view set
router.register(r'tasks', TaskViewSet)
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
)

urlpatterns = [
    path('add-fire-station/', views.add_fire_station, name='add_fire_station'),
    path('fire-stations/', views.fire_station_list, name='fire_station_list'),
    path('police-stations/', views.police_station_list, name='police_station_list'),
    path('add-police-station/', views.add_police_station, name='add_police_station'),
    path('change-password/', views.change_password, name='change_password'),
    path('live-map/', views.live_map_view, name='live_map'),
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
