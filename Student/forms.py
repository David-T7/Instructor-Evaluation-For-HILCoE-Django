from django import forms
from django.forms import ModelForm
from Course.models import Batch, Course, Term
from Instructor.models import Instructor

from Student.models import Student

evaluatorchoice = [
    ( None, '---------'),
    ('Student', 'Student'),
    ('Staff', 'Staff'),
    ('Both' , 'Both'),
    ('Total' , 'Total'),
    
    
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
