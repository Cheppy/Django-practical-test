import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import CV
from main.utils import generate_pdf_sync, generate_pdf
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def cv():
    return CV.objects.create(
        firstname='John',
        lastname='Doe',
        bio='Test Bio',
        contacts='Test Contacts',
        skills='Python, Django',
        projects='Test Project'
    )

@pytest.mark.django_db
def test_cv_pdf_view(client, cv):
    """Test the CV PDF view"""
    # Mock the generate_pdf_sync function
    with patch('main.views.generate_pdf_sync') as mock_generate:
        # Create a mock PDF content
        mock_pdf = b'Mock PDF Content'
        mock_generate.return_value = mock_pdf

        # Make the request
        response = client.get(reverse('cv_pdf', args=[cv.pk]))

        # Check response
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        assert response['Content-Disposition'] == f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
        assert response.content == mock_pdf

@pytest.mark.django_db
def test_cv_pdf_view_not_found(client):
    """Test the CV PDF view with non-existent CV"""
    response = client.get(reverse('cv_pdf', args=[999]))
    assert response.status_code == 404

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_generate_pdf():
    """Test the generate_pdf function"""
    # Create mock browser and page with async methods
    mock_page = AsyncMock()
    mock_browser = AsyncMock()
    mock_browser.newPage.return_value = mock_page

    # Mock PDF generation
    mock_pdf = b'Test PDF Content'
    mock_page.pdf.return_value = mock_pdf

    # Test URL
    test_url = 'http://test.com/cv/1'

    with patch('main.utils.launch', return_value=mock_browser):
        # Call the function
        pdf = await generate_pdf(test_url)

        # Verify the result
        assert pdf == mock_pdf
        
        # Verify browser was launched with correct options
        mock_browser.newPage.assert_called_once()
        mock_page.setViewport.assert_called_once()
        mock_page.goto.assert_called_once_with(
            test_url,
            {'waitUntil': 'networkidle0', 'timeout': 30000}
        )
        mock_page.waitForSelector.assert_called_once_with(
            'body',
            {'timeout': 5000}
        )
        mock_page.pdf.assert_called_once()
        mock_browser.close.assert_called_once()

@pytest.mark.django_db
def test_generate_pdf_sync():
    """Test the generate_pdf_sync function"""
    # Mock the async generate_pdf function
    with patch('main.utils.generate_pdf') as mock_generate:
        # Create a mock PDF content
        mock_pdf = b'Test PDF Content'
        mock_generate.return_value = mock_pdf

        # Test URL
        test_url = 'http://test.com/cv/1'

        # Call the function
        pdf = generate_pdf_sync(test_url)

        # Verify the result
        assert pdf == mock_pdf
        mock_generate.assert_called_once_with(test_url)

@pytest.mark.django_db
def test_generate_pdf_error_handling():
    """Test error handling in PDF generation"""
    # Mock the generate_pdf function to raise an exception
    with patch('main.utils.generate_pdf', side_effect=Exception('Test error')):
        # Test URL
        test_url = 'http://test.com/cv/1'

        # Verify that the exception is propagated
        with pytest.raises(Exception) as exc_info:
            generate_pdf_sync(test_url)
        
        assert str(exc_info.value) == 'Test error' 