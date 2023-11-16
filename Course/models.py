from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.db import models
from Instructor.models import Instructor
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

# Create your models here.
class Course(models.Model):
    Course_id =  models.CharField(max_length=20 , unique=True,primary_key=True)
    CourseName = models.CharField(max_length=20 , null=True , blank=True)
    CourseType = models.CharField(max_length=10 , null=True ,  choices=coursetype , blank=True)
    CreditHour = models.IntegerField(null=True , blank=True)
    Department = models.CharField(max_length=10 , null=True ,  choices=departmentchoice , blank=True)
    Instructors = models.ManyToManyField(Instructor)
    def __str__(self):
        return str(self.Course_id + '(' + self.CourseName +')')

class Term(models.Model):
    Term_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Season = models.CharField(max_length=10 , null=True ,  choices=seasonchoice , blank=True)
    current_year = datetime.now().year
    Year = models.IntegerField(
        default=current_year,
        validators=[
            MinValueValidator(current_year),
            MaxValueValidator(current_year + 1)
        ],
    )
    Courses_Given = models.ManyToManyField(Course)
    EvaluationDone = models.BooleanField(null=True , blank=True)
    def __str__(self):
        return str(self.Season + " " +str(self.Year))
    

