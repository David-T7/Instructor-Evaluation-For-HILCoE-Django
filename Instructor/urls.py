from . import views
from django.urls import path
urlpatterns = [
path('instructor/', views.Instructors, name='instructor'),
]