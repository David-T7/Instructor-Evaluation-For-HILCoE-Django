from django.db import models
from Account.models import Account

# Create your models here.
class Student(models.Model):
    Student_id =  models.CharField(max_length=20 , unique=True,
                          primary_key=True)
    Account_id = models.OneToOneField(Account , on_delete=models.CASCADE ,null=True , blank=True)
    Department = models.CharField(max_length=20 , null=True , blank=True)
    Batch = models.CharField(max_length=20 , null=True , blank=True)
    def __str__(self):
        return str(self.Student_id)