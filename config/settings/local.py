from .base import *
from .base import env


DEBUG = True
SSL_ISSANDBOX = env('SSL_ISSANDBOX')
STORE_ID = env('STORE_ID')
STORE_PASS = env('STORE_PASS')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(',')

THIRD_PARTY_APPS += [
    'debug_toolbar',
]
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Django-Debug-Toolbar
INTERNAL_IPS = env('INTERNAL_IPS').split(',')
