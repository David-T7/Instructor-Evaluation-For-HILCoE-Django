from django import forms
from django.forms import ModelForm

from Student.models import Student

class StudentCreationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['Student_id']