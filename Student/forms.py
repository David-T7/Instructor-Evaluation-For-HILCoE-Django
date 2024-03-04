import json
from django import forms
from django.forms import ModelForm
from Course.models import  Course, Term
from Instructor.models import Instructor

from Student.models import Student

evaluatorchoice = [
    ( None, '---------'),
    ('Student', 'Student'),
    ('Staff', 'Staff'),
    ('Both' , 'Both'),
    ('Total' , 'Total'),
]


general_report_evaluator_choice = [
    ( None, '---------'),
    ('Student', 'Student'),
    ('Staff', 'Staff'),
    ('Total' , 'Total'),
]

coursechoice = [
    ( None, '---------'),
    ('Lecture', 'Lecture'),
    ('Lab', 'Lab'),
]

department =[
    ( None, '---------'),
    ('Computer Science', 'Computer Science'),
    ('Software Engineering', 'Software Engineering'),
    ('Common Course', 'Common Course'),
]

class StudentCreationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['Student_id']


class EvaluationSearchForm(forms.Form):
    Term_id = forms.ModelChoiceField(queryset=Term.objects.all(), required=False)
    Course_id = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    Instructor_id = forms.ModelChoiceField(queryset=Instructor.objects.all(), required=False)
    evaluator = forms.ChoiceField(choices=evaluatorchoice , required=False)
    department = forms.ChoiceField(choices=department , required=False)


class GeneralReportForm (forms.Form):
    Term_id = forms.ModelChoiceField(queryset=Term.objects.all(), required=False)
    evaluator = forms.ChoiceField(choices=general_report_evaluator_choice , required=True)
    course_type = forms.ChoiceField(choices=coursechoice , required=True)
    department = forms.ChoiceField(choices=department , required=True)
    
    
# forms.py
from django import forms

class PDFDownloadForm(forms.Form):
    criteria_average_Scores = forms.CharField(widget=forms.HiddenInput)
    category_average_scores = forms.JSONField(widget=forms.HiddenInput)
    criteria_sections = forms.CharField(widget=forms.HiddenInput)
    instructor_id = forms.CharField(widget=forms.HiddenInput)
    course_id = forms.CharField(widget=forms.HiddenInput)
    active_page = forms.CharField(widget=forms.HiddenInput)
    evaluator = forms.CharField(widget=forms.HiddenInput)
    course_type = forms.CharField(widget=forms.HiddenInput)
    term_id = forms.CharField(widget=forms.HiddenInput)

