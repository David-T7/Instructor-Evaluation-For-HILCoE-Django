from . import views
from django.urls import path
from .views import InstructorHomePage , Instructors , instructor_evaluate_page , instructor_evaluate_course
urlpatterns = [
path('instructor/', Instructors, name='instructor'),
path('instructorhomepage/', InstructorHomePage, name='instructorhomepage'),
path('instructorevaluatepage' , instructor_evaluate_page , name='evaluate_instructor'),
path('instructorevaluate/<str:evaluator_instructor_id>/<str:course_id>/<str:evaluatee_instructor_id>//<str:course_type>/', instructor_evaluate_course, name='instructor_evaluate_course'),
]