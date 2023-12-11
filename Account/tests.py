# tests.py
import random
from django.test import TestCase
from .models import Account
from .forms import CustomUserCreationForm

class AccountModelTest(TestCase):
    def test_create_account(self):
        account = Account.objects.create(
            username='test_user',
            email='test@example.com',
            password='test_password',
            Role = 'Student'
        )
        self.assertEqual(account.username, 'test_user')
        self.assertEqual(account.email, 'test@example.com')
        self.assertEqual(account.Role, 'Student')

class CustomUserCreationFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'test_password',
            'Role': 'Student',  # Select a role randomly
            'email': 'test@example.com',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())


        form_data = {
        'username': 'test_user',
        'password1': 'test_password',
        'password2': 'test2_password',
        'Role': 'Student',  # Select a role randomly
        'email': 'test@example.com',
        }
        form = CustomUserCreationForm(data=form_data)
    
        if not form.is_valid():
            print(form.errors)

        self.assertFalse(form.is_valid(), form.errors.as_text())
