from .base import *
from .base import env


DEBUG = True
SSL_ISSANDBOX = True

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

# This needs to come before 'staticfiles' app
DEFAULT_APPS.insert(0, 'whitenoise.runserver_nostatic')
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Django-Debug-Toolbar
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', '*']
