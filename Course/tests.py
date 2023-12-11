from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from Account.models import Account
from Course.forms import BatchForm

from Instructor.models import Instructor
from .models import Batch, CourseInstructor, Term, departmentchoice, coursetype, season_choices
from django.utils import timezone
from .models import Course
from django.db.utils import IntegrityError

class TermModelTest(TestCase):
    def test_create_term(self):
        # Create a Term instance with valid data
        term = Term.objects.create(
            Season='Spring',
            Year=datetime.now().year,
            Evaluation_Start_Date=datetime.now() - timedelta(days=1),
            Evaluation_End_Date=datetime.now() + timedelta(days=1),
            EvaluationDone=False
        )
        self.assertEqual(term.Season , 'Spring')
        self.assertEqual(term.Year, datetime.now().year)
        self.assertFalse(term.EvaluationDone)

    def test_invalid_evaluation_dates(self):
    # Try to create a Term instance with invalid evaluation dates
        term = Term(
        Season='Spring',
        Year=datetime.now().year,
        Evaluation_Start_Date=timezone.now() + timedelta(days=1),
        Evaluation_End_Date=timezone.now(),
        EvaluationDone=False
        )

        try:
            term.full_clean()
        except ValidationError as e:
            print(e)
            raise  # Re-raise the exception to fail the test



    def test_invalid_year(self):
        # Try to create a Term instance with an invalid year
        term = Term(
            Season='Spring',
            Year=datetime.now().year - 1,
            Evaluation_Start_Date=timezone.now(),
            Evaluation_End_Date=timezone.now() + timedelta(days=1),
            EvaluationDone=False
        )

        with self.assertRaises(ValidationError) as context:
            term.full_clean()

        self.assertIn('Year', context.exception.message_dict)


    def test_valid_season_choices(self):
        # Check that the Season field only allows valid choices
        for choice in season_choices:
            term = Term(Season=choice[0], Year=datetime.now().year)
            term.full_clean()  # Should not raise ValidationError

    def test_invalid_season_choice(self):
        # Try to create a Term instance with an invalid season choice
        with self.assertRaises(ValidationError):
            term = Term(Season='InvalidSeason', Year=datetime.now().year)
            term.full_clean()

#course model testing 
class CourseModelTest(TestCase):
    def test_create_course(self):
        # Create a Course instance with valid data
        course = Course.objects.create(
            Course_id='CS101',
            CourseName='Introduction to Computer Science',
            CreditHour=3
        )
        self.assertEqual(course.Course_id, 'CS101')
        self.assertEqual(course.CourseName, 'Introduction to Computer Science')
        self.assertEqual(course.CreditHour, 3)

    def test_unique_course_id(self):
        # Try to create two courses with the same Course_id (should raise IntegrityError)
        Course.objects.create(
            Course_id='CS101',
            CourseName='Introduction to Computer Science',
            CreditHour=3
        )

        # Attempt to create another course with the same Course_id
        with self.assertRaises(IntegrityError) as context:
            Course.objects.create(
                Course_id='CS101',
                CourseName='Another Course',
                CreditHour=4
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Course_course.Course_id', str(context.exception))

    def test_negative_credit_hour(self):
        # Try to create a course with a negative CreditHour
        course = Course(
            Course_id='CS102',
            CourseName='Advanced Computer Science',
            CreditHour=-2
        )

        # Use a context manager to catch the ValidationError
        with self.assertRaises(ValidationError) as context:
            course.full_clean()

        # Print the validation error for debugging
        print(context.exception)

#Batch test
class BatchModelTest(TestCase):
    def test_create_batch(self):
        # Create a Batch instance with valid data
        batch = Batch.objects.create(Batch='2023')
        self.assertEqual(batch.Batch, '2023')

    def test_batch_str_representation(self):
        # Create a Batch instance
        batch = Batch.objects.create(Batch='2023')

        # Check the string representation
        self.assertEqual(str(batch), '2023')

    def test_create_batch_blank(self):
        # Try to create a Batch instance with blank Batch using the form
        form = BatchForm(data={'Batch': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('Batch', form.errors)
        self.assertEqual(form.errors['Batch'][0], 'This field is required.')



# courseinstructors test
class CourseInstructorModelTest(TestCase):       
    def setUp(self):
        # Create instances for testing
        self.account = Account.objects.create(username='testuser', password='testpassword', Role = 'Instructor', email='test@example.com')
        self.instructor = Instructor.objects.create(
            Instructor_id='I101',
            Account_id=self.account,  # Replace with an actual Account instance if needed
            Title='Dr.',
            FirstName='John',
            LastName='Doe',
            Sex='M'
        )
        self.course = Course.objects.create(
            Course_id='C101',
            CourseName='Introduction to Django',
            CreditHour=3
        )
        self.batch = Batch.objects.create(Batch='BatchA')
         # Create an Account instance for testing
        

    def test_create_course_instructor(self):
        # Create a CourseInstructor instance with valid data
        course_instructor = CourseInstructor.objects.create(
            Instructors=self.instructor,
            Course=self.course,
            CourseType='Lecture',
            Batch=self.batch,
            Department='CS'
        )
        self.assertEqual(course_instructor.Instructors, self.instructor)
        self.assertEqual(course_instructor.Course, self.course)
        self.assertEqual(course_instructor.CourseType, 'Lecture')
        self.assertEqual(course_instructor.Batch, self.batch)
        self.assertEqual(course_instructor.Department, 'CS')
