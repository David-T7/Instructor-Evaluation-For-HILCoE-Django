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

coursechoice = [
    ( None, '---------'),
    ('Lecture', 'Lecture'),
    ('Lab', 'Lab'),
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
class GeneralReportForm (forms.Form):
    Term_id = forms.ModelChoiceField(queryset=Term.objects.all(), required=False)
    evaluator = forms.ChoiceField(choices=evaluatorchoice , required=True)
    course_type = forms.ChoiceField(choices=coursechoice , required=True)
    
# forms.py
from django import forms

class PDFDownloadForm(forms.Form):
    criteria_average_Scores = forms.CharField(widget=forms.HiddenInput)
    criteria_sections = forms.CharField(widget=forms.HiddenInput)
    instructor_id = forms.CharField(widget=forms.HiddenInput)
    course_id = forms.CharField(widget=forms.HiddenInput)
    active_page = forms.CharField(widget=forms.HiddenInput)
    evaluator = forms.CharField(widget=forms.HiddenInput)
    course_type = forms.CharField(widget=forms.HiddenInput)
    term_id = forms.CharField(widget=forms.HiddenInput)
