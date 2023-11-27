import uuid
from django.db import models
from Account.models import Account
from Course.models import Course, Term
from Instructor.models import Instructor
from Course.models import Batch

     
departmentchoice = [
    ( None, 'SelectDepartment'),
    ('CS', 'CS'),
    ('SE', 'SE'),
    ('Both' , 'Both')
]

# Create your models here.
class Student(models.Model):
    Student_id =  models.CharField(max_length=20 , unique=True,
                          primary_key=True)
    Account_id = models.OneToOneField(Account , on_delete=models.CASCADE ,null=True , blank=True)
    Department = models.CharField(max_length=20 , choices=departmentchoice , null=True , blank=True)
    Batch = models.OneToOneField(Batch , on_delete=models.CASCADE ,null=True , blank=True)
    def __str__(self):
        return str(self.Student_id)

class StudentEvaluationResult(models.Model):
    Result_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    Student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    Course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    Instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    CourseType = models.CharField(max_length=20  , null=True , blank=True)
    Term_id = models.ForeignKey(Term, on_delete=models.CASCADE)
    EvaluationResult = models.JSONField()
    EvaluationDone = models.BooleanField(default=False , null=True)

    class Meta:
        # Add a unique constraint to ensure a student can evaluate a course only once
        unique_together = ('Student_id', 'Course_id', 'Term_id' , 'CourseType')
    def __str__(self):
        return str(self.Course_id.CourseName)

class StudentCourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    enrolled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course', 'term')

    def __str__(self):
        return f'{self.student} - {self.course} - Term: {self.term} - Enrolled: {self.enrolled}'


