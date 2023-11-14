from django.urls import path
from .views import  homepage , staffhomepage

urlpatterns = [
path('',  homepage, name='homepage'),
path('staffhomepage', staffhomepage , name='staffhomepage'),
]