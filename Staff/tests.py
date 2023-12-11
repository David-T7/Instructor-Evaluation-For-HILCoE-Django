from django.test import TestCase
from .models import Staff
from Account.models import Account
from .models import StaffEvaluationResult
from Course.models import Course, Term, Instructor
import uuid

class StaffModelTest(TestCase):
    def setUp(self):
        # Create an instance for testing
        self.account1 = Account.objects.create(
            username='staff_member',
            email='staff_member@example.com',
            password='password'  # Replace with a hashed password if needed
        )

    def test_create_staff_member(self):
        # Create a Staff instance with valid data
        staff_member = Staff.objects.create(
            Staff_id='S101',
            FirstName='John',
            LastName='Doe',
            Account_id=self.account1,
            Sex='M'
        )
        self.assertEqual(staff_member.Staff_id, 'S101')
        self.assertEqual(staff_member.FirstName, 'John')
        self.assertEqual(staff_member.LastName, 'Doe')
        self.assertEqual(staff_member.Account_id, self.account1)
        self.assertEqual(staff_member.Sex, 'M')

    def test_str_representation(self):
        # Test the __str__ representation of a Staff instance
        staff_member = Staff.objects.create(
            Staff_id='S102',
            FirstName='Jane',
            LastName='Smith',
            Account_id=self.account1,
            Sex='F'
        )
        expected_str = 'Jane Smith'
        self.assertEqual(str(staff_member), expected_str)

    def test_default_sex_value(self):
        # Create a Staff instance without specifying the sex value (should use the default)
        staff_member = Staff.objects.create(
            Staff_id='S103',
            FirstName='Alex',
            LastName='Johnson',
            Account_id=self.account1
        )
        self.assertIsNone(staff_member.Sex)

    def test_unique_constraint(self):
        # Create a Staff instance
        self.account2 = Account.objects.create(
            username='staff_member2',
            email='staff_member2@example.com',
            password='password'  # Replace with a hashed password if needed
        )
        staff_member = Staff.objects.create(
            Staff_id='S104',
            FirstName='Chris',
            LastName='Williams',
            Account_id=self.account1,
            Sex='M'
        )

        # Attempt to create another Staff with the same staff ID (should raise IntegrityError)
        with self.assertRaises(Exception) as context:
            Staff.objects.create(
                Staff_id='S104',
                FirstName='David',
                LastName='Brown',
                Account_id=self.account2,
                Sex='M'
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Staff_staff.Staff_id', str(context.exception))

class StaffEvaluationResultModelTest(TestCase):
    def setUp(self):
        self.staffaccount = Account.objects.create(
            username='staff_member',
            email='staff_member@example.com',
            password='password'  # Replace with a hashed password if needed
        )
        self.instructoraccount = Account.objects.create(
            username='instructor',
            email='instructor@example.com',
            password='password'  # Replace with a hashed password if needed
        )
        # Create instances for testing
        self.staff_member = Staff.objects.create(
            Staff_id='S201',
            FirstName='John',
            LastName='Doe',
            Account_id=self.staffaccount,  # Replace with an actual Account instance if needed
            Sex='M'
        )
        self.course = Course.objects.create(
            Course_id='C201',
            CourseName='Advanced Staff Evaluation',
            CreditHour=3
        )
        self.instructor = Instructor.objects.create(
            Instructor_id='I201',
            FirstName='Jane',
            LastName='Smith',
            Account_id=self.instructoraccount,  # Replace with an actual Account instance if needed
            Title='Dr.',
            Sex='F'
        )
        self.term = Term.objects.create(
            Term_id=uuid.uuid4(),
            Season='Spring',
            Year=2023,
            Evaluation_Start_Date=None,
            Evaluation_End_Date=None,
            EvaluationDone=False
        )

    def test_create_evaluation_result(self):
        # Create a StaffEvaluationResult instance with valid data
        evaluation_result = StaffEvaluationResult.objects.create(
            Staff_id=self.staff_member,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'rating': 4, 'comments': 'Good job!'},
            AdditionalComment='Overall, the course was well-organized.',
            EvaluationDone=True
        )
        self.assertEqual(evaluation_result.Staff_id, self.staff_member)
        self.assertEqual(evaluation_result.Course_id, self.course)
        self.assertEqual(evaluation_result.Instructor_id, self.instructor)
        self.assertEqual(evaluation_result.CourseType, 'Lab')
        self.assertEqual(evaluation_result.Term_id, self.term)
        self.assertEqual(evaluation_result.EvaluationResult, {'rating': 4, 'comments': 'Good job!'})
        self.assertEqual(evaluation_result.AdditionalComment, 'Overall, the course was well-organized.')
        self.assertTrue(evaluation_result.EvaluationDone)

    def test_str_representation(self):
        # Test the __str__ representation of a StaffEvaluationResult instance
        evaluation_result = StaffEvaluationResult.objects.create(
            Staff_id=self.staff_member,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lecture',
            Term_id=self.term,
            EvaluationResult={'rating': 3, 'comments': 'Average performance.'},
            AdditionalComment='Could be improved in certain areas.',
            EvaluationDone=False
        )
        expected_str = 'Jane'
        self.assertEqual(str(evaluation_result), expected_str)

    def test_default_values(self):
        # Create a StaffEvaluationResult instance without specifying the default values
        evaluation_result = StaffEvaluationResult.objects.create(
            Staff_id=self.staff_member,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'rating': 5, 'comments': 'Excellent!'}
        )
        self.assertFalse(evaluation_result.EvaluationDone)
        self.assertIsNone(evaluation_result.AdditionalComment)

    def test_unique_constraint(self):
        # Create a StaffEvaluationResult instance
        evaluation_result = StaffEvaluationResult.objects.create(
            Staff_id=self.staff_member,
            Course_id=self.course,
            Instructor_id=self.instructor,
            CourseType='Lab',
            Term_id=self.term,
            EvaluationResult={'rating': 4, 'comments': 'Good job!'},
            AdditionalComment='Overall, the course was well-organized.',
            EvaluationDone=True
        )

        # Attempt to create another StaffEvaluationResult with the same staff, course, term, and course type (should raise IntegrityError)
        with self.assertRaises(Exception) as context:
            StaffEvaluationResult.objects.create(
                Staff_id=self.staff_member,
                Course_id=self.course,
                Instructor_id=self.instructor,
                CourseType='Lab',
                Term_id=self.term,
                EvaluationResult={'rating': 3, 'comments': 'Average performance.'},
                AdditionalComment='Could be improved in certain areas.',
                EvaluationDone=False
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('Staff_staffevaluationresult.Staff_id_id, Staff_staffevaluationresult.Course_id_id, Staff_staffevaluationresult.Term_id_id, Staff_staffevaluationresult.CourseType', str(context.exception))