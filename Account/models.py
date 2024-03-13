from django.contrib.auth.models import AbstractUser
from django.db import models


rolechoice = [
    ( None, 'Select Role'),
    ('Student', 'Student'),
    ('Instructor', 'Instructor'),
    ('StaffMember', 'StaffMember'),
    ('AcademicHead','AcademicHead')
    ]

class Account(AbstractUser):
    Role = models.CharField(max_length=25, null=True , choices=rolechoice ,  blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )


    

    
    

