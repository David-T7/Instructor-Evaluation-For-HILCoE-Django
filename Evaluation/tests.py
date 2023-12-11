from django.test import TestCase
from .models import Criteria, CriteriaSection , EvaluationCriteria
import uuid

class CriteriaSectionModelTest(TestCase):
    def test_create_criteria_section(self):
        # Create a CriteriaSection instance with valid data
        section = CriteriaSection.objects.create(Section='Content')
        self.assertEqual(section.Section, 'Content')

    def test_str_representation(self):
        # Test the __str__ representation of a CriteriaSection instance
        section = CriteriaSection.objects.create(Section='Organization')
        expected_str = 'Organization'
        self.assertEqual(str(section), expected_str)

class CriteriaModelTest(TestCase):
    def setUp(self):
        # Create a CriteriaSection instance for testing
        self.criteria_section = CriteriaSection.objects.create(Section='Content')

    def test_create_criteria(self):
        # Create a Criteria instance with valid data
        criteria = Criteria.objects.create(
            Section=self.criteria_section,
            description='Clear and informative content.'
        )
        self.assertEqual(criteria.Section, self.criteria_section)
        self.assertEqual(criteria.description, 'Clear and informative content.')

    def test_str_representation(self):
        # Test the __str__ representation of a Criteria instance
        criteria = Criteria.objects.create(
            Section=self.criteria_section,
            description='Logical structure and flow.'
        )
        expected_str = 'Content-Logical structure and flow.'
        self.assertEqual(str(criteria), expected_str)

class EvaluationCriteriaModelTest(TestCase):
    def setUp(self):
        # Create Criteria instances for testing
        self.section1 = CriteriaSection.objects.create(Section='Content')
        self.section2 = CriteriaSection.objects.create(Section='Organization')
        self.criteria_1 = Criteria.objects.create(Section=self.section1, description='Clear and informative content.')
        self.criteria_2 = Criteria.objects.create(Section=self.section2, description='Logical structure and flow.')

    def test_create_evaluation_criteria(self):
        # Create an EvaluationCriteria instance with valid data
        evaluation_criteria = EvaluationCriteria.objects.create(
            Evaluator='Student',
            Evaluatee='Lecture'
        )
        evaluation_criteria.Criteria_data.add(self.criteria_1)
        evaluation_criteria.Criteria_data.add(self.criteria_2)

        self.assertEqual(evaluation_criteria.Evaluator, 'Student')
        self.assertEqual(evaluation_criteria.Evaluatee, 'Lecture')
        self.assertCountEqual(evaluation_criteria.Criteria_data.all(), [self.criteria_1, self.criteria_2])

    def test_str_representation(self):
        # Test the __str__ representation of an EvaluationCriteria instance
        evaluation_criteria = EvaluationCriteria.objects.create(
            Evaluator='Instructor',
            Evaluatee='Lab'
        )
        evaluation_criteria.Criteria_data.add(self.criteria_1)

        expected_str = 'Instructor evaluation criteria Lab'
        self.assertEqual(str(evaluation_criteria), expected_str)

    