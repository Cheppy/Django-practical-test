import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from main.models import CV
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def cv():
    return CV.objects.create(
        firstname='John',
        lastname='Doe',
        bio='Test Bio',
        skills='Python, Django',
        projects='Test Project',
        contacts='Test Contacts'
    )

@pytest.mark.django_db
class TestCVAPI:
    def test_list_cvs_unauthorized(self, api_client):
        """Test that unauthorized users can list (read) CVs"""
        url = reverse('cv-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_cvs_authorized(self, authenticated_client, cv):
        """Test that authorized users can list CVs and see created data"""
        url = reverse('cv-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['firstname'] == 'John'
        assert response.data['results'][0]['lastname'] == 'Doe'

    def test_create_cv_authorized(self, authenticated_client):
        """Test that authorized users can create a CV"""
        url = reverse('cv-list')
        data = {
            'firstname': 'Jane',
            'lastname': 'Smith',
            'bio': 'Another test bio',
            'skills': 'JavaScript, React',
            'projects': 'Another test project',
            'contacts': 'jane@example.com'
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert CV.objects.count() == 1
        assert response.data['firstname'] == 'Jane'

    def test_create_cv_unauthorized(self, api_client):
        """Test that unauthorized users cannot create a CV"""
        url = reverse('cv-list')
        data = {
            'firstname': 'Unauthorized',
            'lastname': 'User',
            'bio': 'Should not be created',
            'skills': 'None',
            'projects': 'None',
            'contacts': 'unauthorized@example.com'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CV.objects.count() == 0

    def test_retrieve_cv_unauthorized(self, api_client, cv):
        """Test that unauthorized users can retrieve (read) a specific CV"""
        url = reverse('cv-detail', args=[cv.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['firstname'] == 'John'

    def test_retrieve_cv_authorized(self, authenticated_client, cv):
        """Test that authorized users can retrieve a specific CV"""
        url = reverse('cv-detail', args=[cv.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['firstname'] == 'John'

    def test_update_cv_authorized(self, authenticated_client, cv):
        """Test that authorized users can update a CV"""
        url = reverse('cv-detail', args=[cv.id])
        updated_data = {
            'firstname': 'Johnny',
            'lastname': 'Doe',
            'bio': 'Updated bio',
            'skills': 'Python, Django, Testing',
            'projects': 'Updated project',
            'contacts': 'johnny.doe@example.com'
        }
        response = authenticated_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        cv.refresh_from_db()
        assert cv.firstname == 'Johnny'

    def test_update_cv_unauthorized(self, api_client, cv):
        """Test that unauthorized users cannot update a CV"""
        url = reverse('cv-detail', args=[cv.id])
        updated_data = {
            'firstname': 'Unauthorized Update',
            'lastname': 'Doe',
            'bio': 'Should not be updated',
            'skills': 'None',
            'projects': 'None',
            'contacts': 'unauthorized.update@example.com'
        }
        response = api_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        cv.refresh_from_db()
        assert cv.firstname == 'John'

    def test_delete_cv_authorized(self, authenticated_client, cv):
        """Test that authorized users can delete a CV"""
        url = reverse('cv-detail', args=[cv.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CV.objects.count() == 0

    def test_delete_cv_unauthorized(self, api_client, cv):
        """Test that unauthorized users cannot delete a CV"""
        url = reverse('cv-detail', args=[cv.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CV.objects.count() == 1

    def test_invalid_cv_data(self, authenticated_client):
        """Test that invalid CV data is rejected"""
        url = reverse('cv-list')
        data = {
            'firstname': '',
            'lastname': 'Smith',
            'bio': 'Test Bio',
            'skills': 'Python',
            'projects': 'Test Project'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'firstname' in response.data
