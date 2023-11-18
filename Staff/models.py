import uuid
from django.db import models
from Account.models import Account
from Course.models import Course, Term
from Instructor.models import Instructor

genderchoice = [
    ( None, 'SelectGender'),
    ('M', 'M'),
    ('F', 'F'),
]

# Create your models here.
class Staff(models.Model):
    Staff_id =  models.CharField(max_length=20 , unique=True,
                          primary_key=True)
    FirstName =  models.CharField(max_length=20 , null=True , blank=True)
    LastName =  models.CharField(max_length=20 , null=True , blank=True)
    Account_id = models.OneToOneField(Account , on_delete=models.CASCADE ,null=True , blank=True)
    Sex = models.CharField(max_length=25, null=True , choices=genderchoice ,  blank=True)
    def __str__(self):
        return str(self.FirstName + " "+ self.LastName)

class StaffEvaluationResult(models.Model):
    Result_id =  models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    Staff_id = models.ForeignKey(Staff , on_delete=models.CASCADE)
    Course_id = models.ForeignKey(Course , on_delete=models.CASCADE)
    Instructor_id = models.ForeignKey(Instructor , on_delete=models.CASCADE)
    Term_id = models.ForeignKey(Term , on_delete=models.CASCADE)
    EvaluationResult = models.JSONField()
    EvaluationDone = models.BooleanField(default=False , null=True)

    
    class Meta:
        # Add a unique constraint to ensure a student can evaluate a course only once
        unique_together = ('Staff_id', 'Instructor_id', 'Term_id')
    def __str__(self):
        return str(self.Instructor_id.FirstName)
    
class PeerEvaluationResult(models.Model):
    Result_id =  models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    Evaluator_Instructor_id = models.ForeignKey(Instructor , on_delete=models.CASCADE , related_name="evaluator_instructor")
    Course_id = models.ForeignKey(Course , on_delete=models.CASCADE)
    Instructor_id = models.ForeignKey(Instructor , on_delete=models.CASCADE)
    Term_id = models.ForeignKey(Term , on_delete=models.CASCADE)
    EvaluationResult = models.JSONField()
    EvaluationDone = models.BooleanField(default=False , null=True)

    
    class Meta:
        # Add a unique constraint to ensure a student can evaluate a course only once
        unique_together = ('Evaluator_Instructor_id', 'Instructor_id', 'Term_id')
    def __str__(self):
        return str(self.Instructor_id.FirstName)