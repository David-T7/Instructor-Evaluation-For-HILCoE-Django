from django.db import models
from Account.models import Account



genderchoice = [
    ( None, 'SelectGender'),
    ('M', 'M'),
    ('F', 'F'),
]

titlechoice = [
    ( None, 'SelectTitle'),
    ('Mr.', 'Mr.'),
    ('Ms.', 'Ms.'),
    ('Dr.' , 'Dr.'),
    ('Prof.' , 'Prof.')
]

# Create your models here.
class Instructor(models.Model):
    Instructor_id =  models.CharField(max_length=20 , unique=True,primary_key=True)
    Account_id = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='instructor')
    Title = models.CharField(max_length=10 , null=True ,  choices=titlechoice , blank=True)
    FirstName = models.CharField(max_length=20 , null=True , blank=True)
    LastName =  models.CharField(max_length=20 , null=True , blank=True)
    Sex = models.CharField(max_length=25, null=True , choices=genderchoice ,  blank=True)
    ProfilePic= models.FileField(null=True, blank=True, upload_to='profilepic/', default="profilepic/defaultprofile.jpeg")
    def __str__(self):
        return str(self.FirstName + " "+ self.LastName)

