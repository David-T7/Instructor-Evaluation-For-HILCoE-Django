from . import views
from django.urls import path 
from .views import  evaluate_course, studenthomepage , Register , Studnets , student_evaluate_page
urlpatterns = [
path('register',Register , name='register'),
path('student/', Studnets, name='studnet'),
path('studenthomepage', studenthomepage , name='studenthomepage'),
path('evaluate' , student_evaluate_page , name='evaluate'),
path('evaluate/<str:student_id>/<str:course_id>/<str:instructor_id>/<str:course_type>/', evaluate_course, name='evaluate_course'),
]
  