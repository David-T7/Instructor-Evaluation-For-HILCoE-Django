from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Instructor, titlechoice, genderchoice
from Account.models import Account
class InstructorModelTest(TestCase):
    def setUp(self):
        # Create an Account instance for testing
        self.account = Account.objects.create_user(username='testuser', password='testpassword', Role = 'Instructor', email='test@example.com')

    def test_create_instructor(self):
        # Create an Instructor instance with valid data
        instructor = Instructor.objects.create(
            Instructor_id='I101',
            Account_id=self.account,
            Title='Dr.',
            FirstName='John',
            LastName='Doe',
            Sex='M'
        )
        self.assertEqual(instructor.Instructor_id, 'I101')
        self.assertEqual(instructor.Account_id, self.account)
        self.assertEqual(instructor.Title, 'Dr.')
        self.assertEqual(instructor.FirstName, 'John')
        self.assertEqual(instructor.LastName, 'Doe')
        self.assertEqual(instructor.Sex, 'M')

    def test_unique_instructor_id(self):
        self.account2 = Account.objects.create_user(username='testuser2', password='testpassword', Role = 'Instructor', email='test2@example.com')
    # Create an Instructor instance
        Instructor.objects.create(
        Instructor_id='I102',
        Account_id=self.account,
        Title='Prof.',
        FirstName='Jane',
        LastName='Smith',
        Sex='F'
     )

    # Attempt to create another Instructor with the same Instructor_id (should raise IntegrityError)
        with self.assertRaises(IntegrityError) as context:
            Instructor.objects.create(
            Instructor_id='I102',
            Account_id=self.account2,
            Title='Mr.',
            FirstName='Bob',
            LastName='Johnson',
            Sex='M'
            )

        # Check if the error message contains information about the unique constraint
        self.assertIn('UNIQUE constraint failed: Instructor_instructor.Instructor_id', str(context.exception))

    def test_valid_title_and_sex_choices(self):
        # Create an Instructor instance with valid Title and Sex choices
        instructor = Instructor.objects.create(
            Instructor_id='I103',
            Account_id=self.account,
            Title='Mr.',
            FirstName='Sam',
            LastName='Williams',
            Sex='M'
        )
        self.assertEqual(instructor.Title, 'Mr.')
        self.assertEqual(instructor.Sex, 'M')

    def test_upload_profile_pic(self):
        # Create an Instructor instance with a profile picture
        image_data = open('C:\InstructorEvaluationSystem\static\images\profilePic\defaultprofile.jpeg', 'rb').read()
        profile_pic = SimpleUploadedFile('profile.jpg', image_data, content_type='image/jpeg')
        instructor = Instructor.objects.create(
            Instructor_id='I105',
            Account_id=self.account,
            Title='Prof.',
            FirstName='Alex',
            LastName='Taylor',
            Sex='M',
            ProfilePic=profile_pic
        )

        # Check if the profile picture was uploaded successfully
        self.assertIsNotNone(instructor.ProfilePic)