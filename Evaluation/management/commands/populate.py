import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from Account.models import Account
from Instructor.models import Instructor
from Course.models import Batch, Course, CourseInstructor, Term
from Evaluation.models import CriteriaSection, Criteria, EvaluationCriteria
from Student.models import Student, StudentEvaluationResult, StudentCourseEnrollment


class Command(BaseCommand):
    help = "Popuate the database with dummy data for Instructor Evaluation project"

    def add_arguments(self, parser):
        parser.add_argument('--num_accounts', type=int, default=30, help='Number of accounts to create')
        parser.add_argument('--num_instructors', type=int, default=10, help='Number of instructors to create')
        parser.add_argument('--num_students', type=int, default=20, help='Number of students to create')
        parser.add_argument('--num_courses', type=int, default=10, help='Number of courses to create')
        parser.add_argument('--num_terms', type=int, default=2, help='Number of terms to create')

    def handle(self, *args, **options):
        fake = Faker()
        num_accounts = options['num_accounts']
        num_instructors = options['num_instructors']
        num_students = options['num_students']
        num_courses = options['num_courses']
        num_terms = options['num_terms']

        self.stdout.write("Starting database seeding...")

        # --- Clear existing data ---
        # WARNING: Uncomment if you want to wipe the data before seeding
        # StudentEvaluationResult.objects.all().delete()
        # StudentCourseEnrollment.objects.all().delete()
        # Student.objects.all().delete()
        # Instructor.objects.all().delete()
        # CourseInstructor.objects.all().delete()
        # Course.objects.all().delete()
        # Batch.objects.all().delete()
        # Term.objects.all().delete()
        # Account.objects.exclude(is_superuser=True).delete()  # Keep superuser

        # --- Create Accounts (mix of roles) ---
        roles = ['Student', 'Instructor', 'StaffMember', 'AcademicHead']
        accounts = []
        for i in range(num_accounts):
            role = random.choice(roles)
            email = f'user{i}@example.com'
            username = f'user{i}'
            acc, created = Account.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'Role': role,
                    'password': 'pbkdf2_sha256$216000$dummy$hashhere',  # dummy hashed password, change as needed
                    'is_active': True,
                }
            )
            if created:
                acc.set_password('password123')  # set password properly
                acc.save()
            accounts.append(acc)

        self.stdout.write(f"Created {len(accounts)} accounts")

        # --- Create Instructors linked to some Accounts with role 'Instructor' ---
        instructors = []
        instructor_accounts = [a for a in accounts if a.Role == 'Instructor']
        for i in range(num_instructors):
            if i < len(instructor_accounts):
                acc = instructor_accounts[i]
            else:
                # Create additional instructor accounts if not enough
                acc = Account.objects.create_user(
                    username=f'instructor{i}',
                    email=f'instructor{i}@example.com',
                    password='password123',
                    Role='Instructor'
                )
            instructor_id = f"INST{i+1:04d}"
            instructor = Instructor.objects.create(
                Instructor_id=instructor_id,
                Title=random.choice(['Mr.', 'Ms.', 'Dr.', 'Prof.']),
                FirstName=fake.first_name(),
                LastName=fake.last_name(),
                Sex=random.choice(['M', 'F']),
                ProfilePic=None
            )
            instructors.append(instructor)

        self.stdout.write(f"Created {len(instructors)} instructors")

        # --- Create Batches ---
        batches = []
        for i in range(1, 5):
            batch_name = f"Batch {i}"
            batch, _ = Batch.objects.get_or_create(Batch=batch_name)
            batches.append(batch)
        self.stdout.write(f"Created {len(batches)} batches")

        # --- Create Courses ---
        courses = []
        for i in range(num_courses):
            course_id = f"CSE{i+101}"
            course_name = fake.catch_phrase()
            department = random.choice(['Computer Science', 'Software Engineering', 'Common Course'])
            credit_hour = random.randint(2, 5)
            course, _ = Course.objects.get_or_create(
                Course_id=course_id,
                defaults={
                    'CourseName': course_name,
                    'Department': department,
                    'CreditHour': credit_hour,
                }
            )
            courses.append(course)

        self.stdout.write(f"Created {len(courses)} courses")

        # --- Assign instructors to courses with CourseInstructor ---
        course_instructors = []
        course_types = ['Lecture', 'Lab']
        for course in courses:
            # assign 1-2 instructors randomly
            assigned_instructors = random.sample(instructors, k=min(len(instructors), random.randint(1, 2)))
            for inst in assigned_instructors:
                ci = CourseInstructor.objects.create(
                    Instructors=inst,
                    Course=course,
                    CourseType=random.choice(course_types),
                    Batch=random.choice(batches)
                )
                course_instructors.append(ci)

        self.stdout.write(f"Created {len(course_instructors)} course instructors")

        # --- Create Terms ---
        current_year = datetime.now().year
        term_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        terms = []
        for i in range(num_terms):
            season = term_seasons[i % len(term_seasons)]
            start_date = timezone.now() - timedelta(days=90)
            end_date = timezone.now() + timedelta(days=90)
            term, _ = Term.objects.get_or_create(
                Year=current_year,
                Season=season,
                defaults={
                    'Evaluation_Start_Date': start_date,
                    'Evaluation_End_Date': end_date,
                    'EvaluationDone': False,
                }
            )
            # Assign all courses to term's Courses_Given
            term.Courses_Given.set(courses)
            terms.append(term)

        self.stdout.write(f"Created {len(terms)} terms")

        # --- Create Criteria Sections and Criteria ---
        sections = ['Teaching Skills', 'Communication', 'Professionalism', 'Knowledge']
        criteria_objects = []
        for section_name in sections:
            section, _ = CriteriaSection.objects.get_or_create(Section=section_name)
            for i in range(3):  # 3 criteria per section
                desc = fake.sentence(nb_words=6)
                c, _ = Criteria.objects.get_or_create(Section=section, description=desc)
                criteria_objects.append(c)

        self.stdout.write(f"Created {len(criteria_objects)} criteria")

        # --- Create Evaluation Criteria ---
        eval_criteria, _ = EvaluationCriteria.objects.get_or_create(
            Evaluator='Student',
            Evaluatee='Lecture'
        )
        eval_criteria.Criteria_data.set(criteria_objects)
        eval_criteria.save()

        self.stdout.write("Created evaluation criteria")

        # --- Create Students linked to Accounts with role 'Student' ---
        student_accounts = [a for a in accounts if a.Role == 'Student']
        students = []
        for i in range(num_students):
            if i < len(student_accounts):
                acc = student_accounts[i]
            else:
                acc = Account.objects.create_user(
                    username=f'student{i}',
                    email=f'student{i}@example.com',
                    password='password123',
                    Role='Student'
                )
            student_id = f"STUD{i+1:05d}"
            student = Student.objects.create(
                Student_id=student_id,
                Account_id=acc,
                Department=random.choice(['Computer Science', 'Software Engineering']),
                Batch=random.choice(batches)
            )
            students.append(student)

        self.stdout.write(f"Created {len(students)} students")

        # --- Enroll Students to Courses in Terms ---
        enrollments = []
        for student in students:
            # enroll each student in random 2-4 courses for each term
            for term in terms:
                courses_for_term = random.sample(courses, k=random.randint(2, 4))
                for course in courses_for_term:
                    enrollment = StudentCourseEnrollment.objects.create(
                        student=student,
                        course=course,
                        term=term,
                        enrolled=True
                    )
                    enrollments.append(enrollment)

        self.stdout.write(f"Created {len(enrollments)} course enrollments")

        # --- Create Student Evaluation Results ---
        evaluation_results = []
        for student in students:
            for term in terms:
                # get courses enrolled for this student and term
                enrolled_courses = StudentCourseEnrollment.objects.filter(student=student, term=term, enrolled=True)
                for enrollment in enrolled_courses:
                    course = enrollment.course
                    # Find instructors teaching this course
                    instructors_for_course = CourseInstructor.objects.filter(Course=course)
                    for ci in instructors_for_course:
                        # Generate fake evaluation results as a dict {criteria_id: rating}
                        eval_result = {str(c.Criteria_id): random.randint(1, 5) for c in criteria_objects}
                        comment = fake.sentence(nb_words=10)
                        ser = StudentEvaluationResult.objects.create(
                            Student_id=student,
                            Course_id=course,
                            Instructor_id=ci.Instructors,
                            CourseType=ci.CourseType,
                            Term_id=term,
                            EvaluationResult=eval_result,
                            AdditionalComment=comment,
                            EvaluationDone=True
                        )
                        evaluation_results.append(ser)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write(f"Created {len(evaluation_results)} student evaluation results")
