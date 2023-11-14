from django import forms
from django.forms import ModelForm

from .models import Instructor

class StudentCreationForm(ModelForm):
    class Meta:
        model = Instructor
        fields = ['Instructor_id']