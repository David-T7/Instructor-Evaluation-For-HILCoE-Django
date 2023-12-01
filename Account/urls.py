from . import views
from django.urls import path

urlpatterns = [ 
path('login', views.Login , name='login'), 
path('logout' , views.Logout , name='logout') ,
path('editusername' , views.EditUserName , name='editusername' ), 
path('editpassword' , views.EditPassword , name='editpassword'),
]