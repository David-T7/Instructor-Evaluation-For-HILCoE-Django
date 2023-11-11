from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Account.models import Account
from Account.models import StudentInfo

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + ('Role',)

class StudentInfoCreationForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ['Student_id','Department','Batch']