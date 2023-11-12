from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

rolechoice = [
    ( None, 'SelectRole'),
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
    def __str__(self):
        return str(self.id)

class StudentInfo(models.Model):
    Student_id =  models.CharField(max_length=20 , unique=True,
                          primary_key=True)
    Department = models.CharField(max_length=20 , null=True , blank=True)
    Batch = models.CharField(max_length=20 , null=True , blank=True)
    Registered = models.BooleanField(null=True , blank=True)
    def __str__(self):
        return str(self.id)

    
    

