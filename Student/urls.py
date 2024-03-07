from . import views
from django.urls import path 
from .views import  evaluate_course, moreStudentEvaluationDetails, search_evaluation, student_evaluation_reports, studenthomepage , Studnets ,Register, student_evaluate_page , total_evaluation_reports, viewpdf
urlpatterns = [
# path('register',Register , name='register'),
path('student/', Studnets, name='studnet'),
path('studenthomepage', studenthomepage , name='studenthomepage'),
path('evaluate' , student_evaluate_page , name='evaluate'),
path('evaluate/<str:student_id>/<str:course_id>/<str:instructor_id>/<str:course_type>/', evaluate_course, name='evaluate_course'),
path('student-evaluation-reports/<str:evaluator>/', student_evaluation_reports, name='evaluation_reports'),
path( 'total-evaluation-report', total_evaluation_reports  , name='total_evaluation'),
path('morestudnet_evaluation_result/<str:instructor_id>/<str:course_id>/<str:course_type>/<str:evaluator>/<str:term_id>/', moreStudentEvaluationDetails, name='morestudnet_evaluation_result'),
path('search/', search_evaluation, name='search_evaluation') , 
path('viewpdf/', viewpdf, name='viewpdf'),
]
  