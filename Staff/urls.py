from django.urls import path
from .views import  staffhomepage

urlpatterns = [
path('staffhomepage', staffhomepage , name='staffhomepage'),
]