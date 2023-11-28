from django.urls import path
from .views import  stafflandingpage , staffHomePage , staff_evaluate_page , staff_evaluate_course ,academicheadHomePage

urlpatterns = [
path('staff', stafflandingpage , name='stafflandingpage'),
path ('staffhomepage' , staffHomePage , name='staffhomepage'),
path ('academicheadhomepage' , academicheadHomePage , name='academicheadhomepage'),
path('evaluatepage' , staff_evaluate_page , name='evaluate_staff'),
path('staffevaluate/<str:staff_id>/<str:course_id>/<str:instructor_id>/<str:course_type>/', staff_evaluate_course, name='staff_evaluate_course'),

]