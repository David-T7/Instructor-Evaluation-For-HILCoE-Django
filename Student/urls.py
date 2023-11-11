from . import views
from django.urls import path
urlpatterns = [
path('register',views.Register , name='register'),
path('student/', views.Studnets, name='studnet'),
]