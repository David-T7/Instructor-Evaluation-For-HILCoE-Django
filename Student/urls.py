from . import views
from django.urls import path 
from .views import  studenthomepage , Register , Studnets
urlpatterns = [
path('register',Register , name='register'),
path('student/', Studnets, name='studnet'),
path('studenthomepage', studenthomepage , name='studenthomepage'),
]
  