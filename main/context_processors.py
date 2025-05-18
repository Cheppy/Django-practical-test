from django.conf import settings
from django.http import HttpRequest

def settings_context(request: HttpRequest) -> dict:
    """
    Context processor that injects Django settings into templates.
    Only injects settings that are safe to expose in templates.
    """
    safe_settings = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'TIME_ZONE': settings.TIME_ZONE,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'USE_I18N': settings.USE_I18N,
        'USE_TZ': settings.USE_TZ,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'MIDDLEWARE': settings.MIDDLEWARE,
        'TEMPLATES': [
            {
                'BACKEND': template['BACKEND'],
                'NAME': template.get('NAME', ''),
                'DIRS': template.get('DIRS', []),
                'APP_DIRS': template.get('APP_DIRS', False),
            }
            for template in settings.TEMPLATES
        ],
    }
    return {'settings': safe_settings} 