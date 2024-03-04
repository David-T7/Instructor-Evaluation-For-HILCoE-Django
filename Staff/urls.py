from django.urls import path
from .views import  stafflandingpage , staffHomePage , staff_evaluate_page , staff_evaluate_course ,academicheadHomePage , generalEvaluationReport , generate_total_report_excel

urlpatterns = [
path('staff', stafflandingpage , name='stafflandingpage'),
path ('staffhomepage' , staffHomePage , name='staffhomepage'),
path ('academicheadhomepage' , academicheadHomePage , name='academicheadhomepage'),
path('evaluatepage' , staff_evaluate_page , name='evaluate_staff'),
path('staffevaluate/<str:staff_id>/<str:course_id>/<str:instructor_id>/<str:course_type>/', staff_evaluate_course, name='staff_evaluate_course'),
path('evaluationreport/<str:type>', generalEvaluationReport, name='general_evaluation_report'),
path('generate_report_excel' , generate_total_report_excel , name="generate_total_report_excel") ,
]