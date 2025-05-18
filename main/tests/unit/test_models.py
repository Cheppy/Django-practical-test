from django.test import TestCase
from main.models import CV

class CVModelTest(TestCase):
    def setUp(self) -> None:
        self.cv_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'bio': 'Test bio',
            'skills': 'Python, Django, Testing',
            'projects': 'Test project',
            'contacts': 'test@example.com'
        }
        self.cv = CV.objects.create(**self.cv_data)

    def test_cv_creation(self) -> None:
        """Test CV model creation and string representation"""
        self.assertEqual(str(self.cv), f"{self.cv_data['firstname']} {self.cv_data['lastname']}")
        self.assertEqual(self.cv.firstname, self.cv_data['firstname'])
        self.assertEqual(self.cv.lastname, self.cv_data['lastname'])
        self.assertEqual(self.cv.bio, self.cv_data['bio'])
        self.assertEqual(self.cv.skills, self.cv_data['skills'])
        self.assertEqual(self.cv.projects, self.cv_data['projects'])
        self.assertEqual(self.cv.contacts, self.cv_data['contacts'])

    def test_cv_timestamps(self) -> None:
        """Test CV model timestamps"""
        self.assertIsNotNone(self.cv.created_at)
        self.assertIsNotNone(self.cv.updated_at)
        self.assertLessEqual(self.cv.created_at, self.cv.updated_at) 