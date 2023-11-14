from django.db import models
import uuid


class Criteria(models.Model):
    SECTION_CHOICES = [
        ('Course Organization', 'Course Organization'),
        ('Knowledge of the subject matter', 'Knowledge of the subject matter'),
        ('Teaching Methods', 'Teaching Methods'),
        ('Personality Traits', 'Personality Traits'),
        ('Availablity and Support', 'Availablity and Support'),
        # Add more sections as needed
    ]
    Section = models.CharField(max_length=255, choices=SECTION_CHOICES)
    description = models.TextField(null=True)
    def __str__(self):
        return str(self.Section + "-" + self.description )



# Create your models here.
class EvaluationCriteria(models.Model):
    Evaluator_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('StaffMember', 'StaffMember'),
        # Add more sections as needed
    ]
    Evaluatee_CHOICES = [
        ('Lecture Insructor', 'Lecture Insructor'),
        ('Lab Instructor', 'Lab Instructor'),
      
        # Add more sections as needed
    ]
    Criteria_id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    Criteria_data = models.ManyToManyField(Criteria)
    Evaluator = models.CharField(max_length=255, choices=Evaluator_CHOICES , null=True)
    Evaluatee = models.CharField(max_length=255, choices=Evaluatee_CHOICES , null=True)
    def __str__(self):
        return str(self.Evaluatee +" evaluation criteria" )
    
    
    