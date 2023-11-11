from . import views
from django.urls import path

urlpatterns = [ 
path('login/<role>', views.Login , name='login'), 

]