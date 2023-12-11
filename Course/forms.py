from django import forms
from django.core.exceptions import ValidationError
from Course.models import Batch
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['Batch']

    def clean_Batch(self):
        batch = self.cleaned_data.get('Batch')
        if not batch.strip():
            raise ValidationError('This field is required.')
        return batch