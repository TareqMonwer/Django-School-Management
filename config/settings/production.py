from .base import *
from .base import env


DEBUG = False

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(',')

DEFAULT_APPS.insert(0, 'whitenoise.runserver_nostatic')
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
