from django.test import TestCase, Client
from django.urls import reverse
from main.models import CV

class CVListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cv1 = CV.objects.create(
            firstname="John",
            lastname="Doe",
            bio="First test bio",
            skills="Python, Django",
            projects="First project",
            contacts="john@example.com"
        )
        self.cv2 = CV.objects.create(
            firstname="Jane",
            lastname="Smith",
            bio="Second test bio",
            skills="JavaScript, React",
            projects="Second project",
            contacts="jane@example.com"
        )

    def test_list_view_status_code(self):
        """Test list view returns 200 status code"""
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Test list view uses correct template"""
        response = self.client.get(reverse('cv_list'))
        self.assertTemplateUsed(response, 'main/cv_list.html')

    def test_list_view_content(self):
        """Test list view displays all CVs"""
        response = self.client.get(reverse('cv_list'))
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")
        self.assertContains(response, "First test bio")
        self.assertContains(response, "Second test bio")
        self.assertContains(response, "Python")
        self.assertContains(response, "JavaScript")

    def test_list_view_ordering(self):
        """Test CVs are ordered by creation date (newest first)"""
        response = self.client.get(reverse('cv_list'))
        content = response.content.decode()
        self.assertLess(
            content.find("Jane Smith"),
            content.find("John Doe")
        )


class CVDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            bio="Test bio",
            skills="Python, Django, Testing",
            projects="Test project",
            contacts="test@example.com"
        )

    def test_detail_view_status_code(self):
        """Test detail view returns 200 status code for existing CV"""
        response = self.client.get(reverse('cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_404(self):
        """Test detail view returns 404 for non-existent CV"""
        response = self.client.get(reverse('cv_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template(self):
        """Test detail view uses correct template"""
        response = self.client.get(reverse('cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertTemplateUsed(response, 'main/cv_detail.html')

    def test_detail_view_content(self):
        """Test detail view displays all CV information"""
        response = self.client.get(reverse('cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Test bio")
        self.assertContains(response, "Python")
        self.assertContains(response, "Django")
        self.assertContains(response, "Test project")
        self.assertContains(response, "test@example.com") 