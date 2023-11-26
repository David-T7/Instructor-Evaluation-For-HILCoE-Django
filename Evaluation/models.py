from django.db import models
import uuid


class CriteriaSection(models.Model):
    Section = models.CharField(max_length=255 )
    def __str__(self):
        return str(self.Section)
    



class Criteria(models.Model):
    Criteria_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Section = models.ForeignKey(CriteriaSection , on_delete=models.CASCADE) 
    description = models.TextField(null=True)
    def __str__(self):
        return str(self.Section.Section + "-" + self.description )



# Create your models here.
class EvaluationCriteria(models.Model):
    Evaluator_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('StaffMember', 'StaffMember'),
        # Add more sections as needed
    ]
    Evaluatee_CHOICES = [
        ('Lecture', 'Lecture'),
        ('Lab', 'Lab'),
      
        # Add more sections as needed
    ]
    EvaluationCriteria_id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    Criteria_data = models.ManyToManyField(Criteria)
    Evaluator = models.CharField(max_length=255, choices=Evaluator_CHOICES , null=True)
    Evaluatee = models.CharField(max_length=255, choices=Evaluatee_CHOICES , null=True)
    def __str__(self):
        return str(self.Evaluator +" evaluation criteria" )
    
    
    