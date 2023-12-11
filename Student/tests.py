from django.test import TestCase
from .models import Student
from Account.models import Account
from Course.models import Batch
from .models import StudentCourseEnrollment
from Course.models import Course, Term , Instructor
import uuid
from .models import StudentEvaluationResult

class StudentModelTest(TestCase):
    def setUp(self):
        # Create instances for testing
        self.account = Account.objects.create(
            username='testuser',
            email='test@example.com'
        )
        self.batch = Batch.objects.create(Batch='BatchA')

    def test_create_student(self):
        # Create a Student instance with valid data
        student = Student.objects.create(
            Student_id='S101',
            Account_id=self.account,
            Department='CS',
            Batch=self.batch
        )
        self.assertEqual(student.Student_id, 'S101')
        self.assertEqual(student.Account_id, self.account)
        self.assertEqual(student.Department, 'CS')
        self.assertEqual(student.Batch, self.batch)

    def test_str_representation(self):
        # Test the __str__ representation of a Student instance
        student = Student.objects.create(
            Student_id='S102',
            Account_id=self.account,
            Department='SE',
            Batch=self.batch
        )
        expected_str = 'S102'
        self.assertEqual(str(student), expected_str)

    
    def test_unique_constraint(self):
        # Create a Student instance
        student = Student.objects.create(
            Student_id='S104',
            Account_id=self.account,
            Department='CS',
            Batch=self.batch
        )

        # Attempt to create another Student with the same Student_id and Batch (should raise IntegrityError)
        with self.assertRaises(Exception) as context:
            Student.objects.create(
                Student_id='S104',
                Account_id=self.account,
                Department='SE',
                Batch=self.batch
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Student_student.Student_id, Student_student.Batch_id', str(context.exception))



class StudentCourseEnrollmentModelTest(TestCase):
    def setUp(self):
        # Create instances for testing
        self.account =  Account.objects.create(
            username='test_user',
            email='test@example.com',
            password='test_password',
            Role = 'Student'
        )
        self.batch = Batch.objects.create(Batch='2023')
        self.student = Student.objects.create(
            Student_id='S201',
            Account_id=self.account,  # Replace with an actual Account instance if needed
            Department='CS',
            Batch=self.batch  # Replace with an actual Batch instance if needed
        )
        self.course = Course.objects.create(
            Course_id='C201',
            CourseName='Advanced Django',
            CreditHour=3
        )
        self.term = Term.objects.create(
            Term_id=uuid.uuid4(),
            Season='Spring',
            Year=2023,
            Evaluation_Start_Date=None,
            Evaluation_End_Date=None,
            EvaluationDone=False
        )

    def test_create_enrollment(self):
        # Create a StudentCourseEnrollment instance with valid data
        enrollment = StudentCourseEnrollment.objects.create(
            student=self.student,
            course=self.course,
            term=self.term,
            enrolled=True
        )
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.term, self.term)
        self.assertTrue(enrollment.enrolled)

    def test_str_representation(self):
        # Test the __str__ representation of a StudentCourseEnrollment instance
        enrollment = StudentCourseEnrollment.objects.create(
            student=self.student,
            course=self.course,
            term=self.term,
            enrolled=False
        )
        expected_str = f'{self.student} - {self.course} - Term: {self.term} - Enrolled: False'
        self.assertEqual(str(enrollment), expected_str)

    def test_default_enrolled_value(self):
        # Create a StudentCourseEnrollment instance without specifying the enrolled value (should use the default)
        enrollment = StudentCourseEnrollment.objects.create(
            student=self.student,
            course=self.course,
            term=self.term
        )
        self.assertFalse(enrollment.enrolled)

    def test_unique_constraint(self):
        # Create a StudentCourseEnrollment instance
        enrollment = StudentCourseEnrollment.objects.create(
            student=self.student,
            course=self.course,
            term=self.term,
            enrolled=True
        )

        # Attempt to create another StudentCourseEnrollment with the same student, course, and term (should raise IntegrityError)
        with self.assertRaises(Exception) as context:
            StudentCourseEnrollment.objects.create(
                student=self.student,
                course=self.course,
                term=self.term,
                enrolled=False
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Student_studentcourseenrollment.student_id, Student_studentcourseenrollment.course_id, Student_studentcourseenrollment.term_id', str(context.exception))

class StudentEvaluationResultModelTest(TestCase):
    def setUp(self):
        # Create instances for testing
        self.studentaccount =  Account.objects.create(
            username='test_user',
            email='test@example.com',
            password='test_password',
            Role = 'Student'
        )
        self.instructoraccount = Account.objects.create_user(username='testuser', password='testpassword', Role = 'Instructor', email='test1@example.com')
        self.batch = Batch.objects.create(Batch='2023')
        
        self.student = Student.objects.create(
            Student_id='S301',
            Account_id=self.studentaccount,  # Replace with an actual Account instance if needed
            Department='CS',
            Batch=self.batch # Replace with an actual Batch instance if needed
        )
        self.course = Course.objects.create(
            Course_id='C301',
            CourseName='Advanced Python',
            CreditHour=4
        )
        self.instructor = Instructor.objects.create(
            Instructor_id='I301',
            Account_id=self.instructoraccount,  # Replace with an actual Account instance if needed
            Title='Dr.',
            FirstName='Jane',
            LastName='Doe',
            Sex='F'
        )
        self.term = Term.objects.create(
            Term_id=uuid.uuid4(),
            Season='Fall',
            Year=2022,
            Evaluation_Start_Date=None,
            Evaluation_End_Date=None,
            EvaluationDone=False
        )

    def test_create_evaluation_result(self):
        # Create a StudentEvaluationResult instance with valid data
        evaluation_result = StudentEvaluationResult.objects.create(
            Student_id=self.student,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lecture',
            Term_id=self.term,
            EvaluationResult={'rating': 4, 'comments': 'Good job!'},
            AdditionalComment='Overall, the course was well-organized.',
            EvaluationDone=True
        )
        self.assertEqual(evaluation_result.Student_id, self.student)
        self.assertEqual(evaluation_result.Course_id, self.course)
        self.assertEqual(evaluation_result.Instructor_id, self.instructor)
        self.assertEqual(evaluation_result.CourseType, 'Lecture')
        self.assertEqual(evaluation_result.Term_id, self.term)
        self.assertEqual(evaluation_result.EvaluationResult, {'rating': 4, 'comments': 'Good job!'})
        self.assertEqual(evaluation_result.AdditionalComment, 'Overall, the course was well-organized.')
        self.assertTrue(evaluation_result.EvaluationDone)

    def test_str_representation(self):
        # Test the __str__ representation of a StudentEvaluationResult instance
        evaluation_result = StudentEvaluationResult.objects.create(
            Student_id=self.student,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'rating': 3, 'comments': 'Average performance.'},
            AdditionalComment='Could be improved in certain areas.',
            EvaluationDone=False
        )
        expected_str = 'Advanced Python'
        self.assertEqual(str(evaluation_result), expected_str)

    def test_default_values(self):
        # Create a StudentEvaluationResult instance without specifying the default values
        evaluation_result = StudentEvaluationResult.objects.create(
            Student_id=self.student,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'rating': 5, 'comments': 'Excellent!'}
        )
        self.assertFalse(evaluation_result.EvaluationDone)
        self.assertIsNone(evaluation_result.AdditionalComment)

    def test_unique_constraint(self):
        # Create a StudentEvaluationResult instance
        evaluation_result = StudentEvaluationResult.objects.create(
            Student_id=self.student,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lecture',
            Term_id=self.term,
            EvaluationResult={'rating': 4, 'comments': 'Good job!'},
            AdditionalComment='Overall, the course was well-organized.',
            EvaluationDone=True
        )

        # Attempt to create another StudentEvaluationResult with the same student, course, term, and course type (should raise IntegrityError)
        with self.assertRaises(Exception) as context:
            StudentEvaluationResult.objects.create(
                Student_id=self.student,
                Course_id=self.course,
                Instructor_id=self.instructor,
                CourseType='Lecture',
                Term_id=self.term,
                EvaluationResult={'rating': 3, 'comments': 'Average performance.'},
                AdditionalComment='Could be improved in certain areas.',
                EvaluationDone=False
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Student_studentevaluationresult.Student_id_id, Student_studentevaluationresult.Course_id_id, Student_studentevaluationresult.Term_id_id, Student_studentevaluationresult.CourseType', str(context.exception))