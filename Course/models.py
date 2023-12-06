from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.db import models
from django.forms import ValidationError
from Instructor.models import Instructor
from django.utils import timezone


departmentchoice = [
    ( None, 'SelectDepartment'),
    ('CS', 'CS'),
    ('SE', 'SE'),
    ('Both' , 'Both')
]

coursetype = [
    ( None, 'CourseType'),
    ('Lecture', 'Lecture'),
    ('Lab', 'Lab'),
]

seasonchoice = [
    ( None, 'SelectSeason'),
    ('spring', 'spring'),
    ('summer', 'summer'),
    ('fall' , 'fall'),
    ('winter' , 'winter'),
]

class Batch(models.Model):
    Batch = models.CharField(max_length=20 , null=True , blank=True)
    def __str__(self):
        return str(self.Batch)

# Create your models here.
class Course(models.Model):
    Course_id =  models.CharField(max_length=20 , unique=True,primary_key=True)
    CourseName = models.CharField(max_length=20 , null=True , blank=True)
    CreditHour = models.IntegerField(null=True , blank=True)
    def __str__(self):
        return str(self.Course_id + '(' + self.CourseName +')')

class CourseInstructor(models.Model):
    Instructors = models.ForeignKey(Instructor , on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    CourseType = models.CharField(max_length=10 , null=True ,  choices=coursetype , blank=True)
    Batch = models.ForeignKey(Batch , on_delete=models.CASCADE ,null=True , blank=True)
    Department = models.CharField(max_length=10 , null=True ,   choices=departmentchoice , blank=True)
    def __str__(self):
        return str(self.Course.CourseName + '(' + self.CourseType + ') :-' + self.Instructors.FirstName  + ' ' +self.Instructors.LastName )
    
    

class Term(models.Model):
    Term_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    season_choices = [("Spring", "Spring"), ("Summer", "Summer"), ("Fall", "Fall"), ("Winter", "Winter")]
    Season = models.CharField(max_length=10, null=True, choices=season_choices, blank=True)
    
    current_year = datetime.now().year
    Year = models.IntegerField(
        default=current_year,
        validators=[
            MinValueValidator(current_year),
            MaxValueValidator(current_year + 1)
        ],
    )

    Evaluation_Start_Date = models.DateTimeField(null=True, blank=True , 
                                                 validators=[MinValueValidator(limit_value=timezone.now())])
    Evaluation_End_Date = models.DateTimeField(null = True , blank=True , 
                                               validators=[MinValueValidator(limit_value=timezone.now())])
    Courses_Given = models.ManyToManyField(Course)
    EvaluationDone = models.BooleanField(null=True, blank=True , default=False)
 
    def __str__(self):
        return str(self.Season + " " + str(self.Year))

    

