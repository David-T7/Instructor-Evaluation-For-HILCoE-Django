from django.test import TestCase
from Student.models import Student
from Account.models import Account
from Course.models import Batch
from Student.models import StudentCourseEnrollment
from Course.models import Course, Term , Instructor , CourseInstructor
import uuid
from Staff.models import Staff , StaffEvaluationResult 
from Evaluation.models import Criteria , CriteriaSection , EvaluationCriteria
from Student.models import StudentEvaluationResult 
from datetime import datetime, timedelta

class IntegrationTest(TestCase):
    def setUp(self):
        # Create some sample data for testing
        self.account = Account.objects.create(username='testuser', email='test@example.com')
        self.instructor = Instructor.objects.create(
            Instructor_id=str(uuid.uuid4()),
            Account_id=self.account,
            FirstName='John',
            LastName='Doe',
            Sex='M'
        )
        self.course = Course.objects.create(Course_id='CS101', CourseName='Introduction to Computer Science', CreditHour=3)
        self.batch = Batch.objects.create(Batch='2023A')
        self.term = Term.objects.create(
            Season='Spring',
            Year=datetime.now().year,
            Evaluation_Start_Date=datetime.now() - timedelta(days=1),
            Evaluation_End_Date=datetime.now() + timedelta(days=1),
            EvaluationDone=False
        )
        self.criteria_section = CriteriaSection.objects.create(Section='Content')
        self.criteria = Criteria.objects.create(Section=self.criteria_section, description='Clear and informative content.')
        self.student = Student.objects.create(Student_id='S123', Account_id=self.account, Department='CS', Batch=self.batch)

    def test_course_instructor_integration(self):
        # Test the integration between Course and Instructor through CourseInstructor
        course_instructor = CourseInstructor.objects.create(
            Instructors=self.instructor,
            Course=self.course,
            CourseType='Lecture',
            Batch=self.batch,
            Department='CS'
        )
        self.assertEqual(course_instructor.Course, self.course)
        self.assertEqual(course_instructor.Instructors, self.instructor)

    def test_term_course_integration(self):
        # Test the integration between Term and Course through EvaluationCriteria
        evaluation_criteria = EvaluationCriteria.objects.create(
            Evaluator='Student',
            Evaluatee='Lecture'
        )
        evaluation_criteria.Criteria_data.add(self.criteria)
        self.assertEqual(evaluation_criteria.Criteria_data.first(), self.criteria)

    def test_student_enrollment_integration(self):
        self.account2 = Account.objects.create(username='testuser2', email='test2@example.com')
        # Test the integration between Student and Course through StudentCourseEnrollment
        student = Student.objects.create(Student_id='S1232', Account_id=self.account2, Department='CS', Batch=self.batch)
        student_enrollment = StudentCourseEnrollment.objects.create(
            student=student,
            course=self.course,
            term=self.term,
            enrolled=True
        )
        self.assertEqual(student_enrollment.student, student)
        self.assertEqual(student_enrollment.course, self.course)

    def test_student_evaluation_result_integration(self):
        # Test the integration between Student, Course, Instructor, and Term through StudentEvaluationResult
        student_evaluation_result = StudentEvaluationResult.objects.create(
            Student_id=self.student,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lecture',
            Term_id=self.term,
            EvaluationResult={'criteria_1': 5, 'criteria_2': 4},
            AdditionalComment='Good job!',
            EvaluationDone=True
        )
        self.assertEqual(student_evaluation_result.Student_id, self.student)
        self.assertEqual(student_evaluation_result.Course_id, self.course)
        self.assertEqual(student_evaluation_result.Instructor_id, self.instructor)
        self.assertEqual(student_evaluation_result.Term_id, self.term)

    def test_staff_evaluation_result_integration(self):
        # Test the integration between Staff, Course, Instructor, and Term through StaffEvaluationResult
        staff = Staff.objects.create(Staff_id='ST123', FirstName='Staff', LastName='Member', Account_id=self.account, Sex='M')
        staff_evaluation_result = StaffEvaluationResult.objects.create(
            Staff_id=staff,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'criteria_1': 4, 'criteria_2': 3},
            AdditionalComment='Needs improvement.',
            EvaluationDone=True
        )
        self.assertEqual(staff_evaluation_result.Staff_id, staff)
        self.assertEqual(staff_evaluation_result.Course_id, self.course)
        self.assertEqual(staff_evaluation_result.Instructor_id, self.instructor)
        self.assertEqual(staff_evaluation_result.Term_id, self.term)
