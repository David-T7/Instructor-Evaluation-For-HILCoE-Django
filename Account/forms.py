from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , PasswordResetForm,SetPasswordForm
from Account.models import Account
from Account.models import StudentInfo

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + ('Role','email')

class StudentInfoCreationForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ['Student_id','Department','Batch']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username']
class CustomEmailChangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email']

class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "enter email-id"
    }))


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
    }))

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
    }))