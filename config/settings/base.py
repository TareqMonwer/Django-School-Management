import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages

from django_school_management.accounts.constants import AccountURLConstants
from utilities.constants import settings_message_constants


######################## Django Core & Custom Configs ########################
##############################################################################

BASE_DIR = Path(__file__).parent.parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    USE_CELERY_REDIS=(bool, False),
    USE_PAYMENT_OPTIONS=(bool, True),
    USE_SENTRY=(bool, False),
    USE_MAILCHIMP=(bool, False),
    SSL_ISSANDBOX=(bool, True),
)
# reading .env file
env.read_env(str(BASE_DIR / "envs/.env"))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

try:
    DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL')
except ImproperlyConfigured:
    DJANGO_ADMIN_URL = 'admin'

DEFAULT_APPS = [
    'django_school_management.accounts.apps.AccountsConfig',  # must be on top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth required
    'django.contrib.sites',
]

LOCAL_APPS = [
    'django_school_management.students.apps.StudentsConfig',
    'django_school_management.teachers.apps.TeachersConfig',
    'django_school_management.result.apps.ResultConfig',
    'django_school_management.academics.apps.AcademicsConfig',
    'django_school_management.pages.apps.PagesConfig',
    'django_school_management.articles.apps.ArticlesConfig',
    'django_school_management.institute.apps.InstituteConfig',
    'django_school_management.payments.apps.PaymentsConfig',
    'django_school_management.notices.apps.NoticesConfig',
]

# third party apps
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap4',
    'rolepermissions',
    'taggit',
    'django_extensions',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'widget_tweaks',
    'django_social_share',
    'django_countries',
    'import_export',
    # 'admin_honeypot',   # admin_honeypot doesn't support Django 4
    'django_tables2',
    'bootstrap4',
    'django_file_form',
    'tinymce',
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # attach_institute_data_ctx_processor was implemented for same support.
    # 'institute.middleware.AttachInstituteDataMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ctx processeor to attach institute data in templates
                'context_processors.dj_sms_context_processor.attach_institute_data_ctx_processor',
                'context_processors.dj_sms_context_processor.attach_urls_for_common_templates',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': env.db(),
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': f'{env("REDIS_HOST")}:{env("REDIS_PORT")}',
    },
}

# Write session to the DB, only load it from the cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# SET MYSQLDB charset for storing Bengali text
if 'mysql' in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Validators are opted out intentionally,
        # please customize this as per your application requirements.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(BASE_DIR / 'static')
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}

MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# login/register redirects

LOGIN_REDIRECT_URL = AccountURLConstants.profile_complete
LOGOUT_REDIRECT_URL = 'account_login'

LOGIN_URL = AccountURLConstants.profile_complete
LOGOUT_URL = 'account_logout'


######################## Third Party Configs ########################
#####################################################################

# DRF CONFIGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

CORS_ALLOW_ALL_ORIGINS = True

# SENTRY - For loggin and monitoring purposes
USE_SENTRY = env('USE_SENTRY')
if USE_SENTRY:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        # debug=True will work even if the DEBUG=False in Django.
        debug=True
    )

# for permission management
ROLEPERMISSIONS_MODULE = 'django_school_management.academics.roles'
# ROLEPERMISSIONS_REGISTER_ADMIN = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_UPLOAD_PATH = 'ck-uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ['codesnippet', 'markdown'], 'width': '100%',
    },
}

# STOP SENDING EMAIL FOR USER REGISTRATION
ACCOUNT_EMAIL_VERIFICATION = 'none'   # use 'mandatory' or 'optional' for respective cases.

# Django taggit.
TAGGIT_CASE_INSENSITIVE = True

# =========================== PAYMENTS ===========================
# BRAINTREE FOR HANDLING PAYMENTS
USE_PAYMENT_OPTIONS = env('USE_PAYMENT_OPTIONS')

if USE_PAYMENT_OPTIONS:
    try:
        # Braintree
        BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
        BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
        BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')

        # SSLCommerz
        STORE_ID = env('STORE_ID')
        STORE_PASS = env('STORE_PASS')
        SSL_ISSANDBOX = env('SSL_ISSANDBOX')
    except ImproperlyConfigured:
        raise ImproperlyConfigured(settings_message_constants.INCORRECT_PAYMENT_GATEWAY_SETUP_MESSAGE)

# CELERY BROKER CONFIG
USE_CELERY_REDIS = env('USE_CELERY_REDIS')

if USE_CELERY_REDIS:
    try:
        CELERY_BROKER_URL = env('CELERY_BROKER_URL')
        CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'Asia/Dhaka'
    except ImproperlyConfigured:
        raise ImproperlyConfigured(settings_message_constants.INCORRECT_CELERY_REDIS_SETUP_MESSAGE)

# MAILCHIMP INTEGRATION
USE_MAILCHIMP = env('USE_MAILCHIMP')
if USE_MAILCHIMP:
    MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
    MAILCHIMP_DATA_CENTER = env('MAILCHIMP_DATA_CENTER')
    MAILCHIMP_LIST_ID = env('MAILCHIMP_LIST_ID')

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
}
