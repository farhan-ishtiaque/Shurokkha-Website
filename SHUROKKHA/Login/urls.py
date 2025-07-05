

from django.urls import path
from . import views as l
urlpatterns = [
     path('l/', l.login), 
]
