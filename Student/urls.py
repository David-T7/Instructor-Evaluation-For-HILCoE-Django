from . import views
from django.urls import path 
from .views import  evaluate_course, moreStudentEvaluationDetails, search_evaluation, student_evaluation_reports, studenthomepage , Register , Studnets , student_evaluate_page
urlpatterns = [
path('register',Register , name='register'),
path('student/', Studnets, name='studnet'),
path('studenthomepage', studenthomepage , name='studenthomepage'),
path('evaluate' , student_evaluate_page , name='evaluate'),
path('evaluate/<str:student_id>/<str:course_id>/<str:instructor_id>/<str:course_type>/', evaluate_course, name='evaluate_course'),
path('student-evaluation-reports/<str:evaluator>/', student_evaluation_reports, name='student_evaluation_reports'),
path('morestudnet_evaluation_result/<str:instructor_id>/<str:course_id>/<str:course_type>/<str:evaluator>/', moreStudentEvaluationDetails, name='morestudnet_evaluation_result'),
path('search/', search_evaluation, name='search_evaluation')
]
  