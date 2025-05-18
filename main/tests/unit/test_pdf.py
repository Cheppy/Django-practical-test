import pytest
from django.urls import reverse
from django.test import Client
from main.models import CV
from main.utils import generate_pdf_sync, generate_pdf
from unittest.mock import patch, AsyncMock
from django.http import HttpResponse

@pytest.fixture
def client() -> Client:
    return Client()

@pytest.fixture
def cv() -> CV:
    return CV.objects.create(
        firstname='John',
        lastname='Doe',
        bio='Test Bio',
        contacts='Test Contacts',
        skills='Python, Django',
        projects='Test Project'
    )

@pytest.mark.django_db
class TestPDFGeneration:
    def test_cv_pdf_view(self, client: Client, cv: CV) -> None:
        """Test the CV PDF view"""
        with patch('main.views.generate_pdf_sync') as mock_generate:
            mock_pdf = b'Mock PDF Content'
            mock_generate.return_value = mock_pdf

            response = client.get(reverse('cv_pdf', args=[cv.pk]))

            assert response.status_code == 200
            assert response['Content-Type'] == 'application/pdf'
            assert response['Content-Disposition'] == f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
            assert response.content == mock_pdf

    def test_cv_pdf_view_not_found(self, client: Client) -> None:
        """Test the CV PDF view with non-existent CV"""
        response = client.get(reverse('cv_pdf', args=[999]))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_pdf_async(self) -> None:
        """Test the generate_pdf async function directly in an async test environment"""
        mock_page = AsyncMock()
        mock_browser = AsyncMock()
        mock_browser.newPage.return_value = mock_page

        mock_pdf = b'Test PDF Content'
        mock_page.pdf.return_value = mock_pdf

        test_url = 'http://test.com/cv/1'

        with patch('main.utils.launch', return_value=mock_browser) as mock_launch:
            pdf = await generate_pdf(test_url)

            mock_launch.assert_awaited_once_with(
                headless=True,
                handleSIGINT=False,
                handleSIGTERM=False,
                handleSIGHUP=False,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--no-zygote',
                    '--single-process'
                ]
            )

            mock_browser.newPage.assert_awaited_once()
            mock_page.setViewport.assert_awaited_once_with({'width': 1200, 'height': 1600})
            mock_page.goto.assert_awaited_once_with(test_url, {'waitUntil': 'networkidle0', 'timeout': 30000})
            mock_page.waitForSelector.assert_awaited_once_with('body', {'timeout': 5000})
            mock_page.pdf.assert_awaited_once()
            mock_browser.close.assert_awaited_once()

            assert pdf == mock_pdf

    def test_generate_pdf_sync(self) -> None:
        """Test the generate_pdf_sync function"""
        with patch('main.utils.generate_pdf') as mock_generate:
            mock_pdf = b'Test PDF Content'
            mock_generate.return_value = mock_pdf

            test_url = 'http://test.com/cv/1'

            pdf = generate_pdf_sync(test_url)

            assert pdf == mock_pdf
            mock_generate.assert_called_once_with(test_url)

    def test_generate_pdf_error_handling(self) -> None:
        """Test error handling in PDF generation"""
        with patch('main.utils.generate_pdf', side_effect=Exception('Test error')):
            test_url = 'http://test.com/cv/1'

            with pytest.raises(Exception) as exc_info:
                generate_pdf_sync(test_url)
            
            assert str(exc_info.value) == 'Test error' 