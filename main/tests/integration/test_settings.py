from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class SettingsViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

    def test_settings_view_authenticated(self) -> None:
        """Test authenticated access to settings view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/settings.html')

    def test_settings_view_unauthenticated(self) -> None:
        """Test unauthenticated access to settings view redirects to login"""
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('settings')}")

    def test_settings_context_processor(self) -> None:
        """Test that settings context processor injects settings"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('settings'))

        self.assertIn('settings', response.context)

        context_settings = response.context['settings']
        self.assertIn('DEBUG', context_settings)
        self.assertEqual(context_settings['DEBUG'], settings.DEBUG)
        self.assertIn('ALLOWED_HOSTS', context_settings)
        self.assertEqual(context_settings['ALLOWED_HOSTS'], settings.ALLOWED_HOSTS)
        self.assertIn('INSTALLED_APPS', context_settings)
        self.assertEqual(list(context_settings['INSTALLED_APPS']), list(settings.INSTALLED_APPS))
        self.assertIn('MIDDLEWARE', context_settings)
        self.assertEqual(list(context_settings['MIDDLEWARE']), list(settings.MIDDLEWARE)) 