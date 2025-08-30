import os
from pathlib import Path
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from decouple import config

import cloudinary
import cloudinary.uploader
import cloudinary.api

import sentry_sdk

from .unfold import UNFOLD

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', config('SECRET_KEY'))

DEBUG = os.getenv('DEBUG', config('DEBUG')) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', config('ALLOWED_HOSTS')).split(',')

CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS', config('CSRF_TRUSTED_ORIGINS', [])
).split(',')

CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', config('CORS_ALLOWED_ORIGINS')
).split(',')

OPENAI_API_KEY = os.getenv(
    'OPENAI_API_KEY', config('OPENAI_API_KEY')
)

LANGSMITH_API_KEY=os.getenv(
    'LANGSMITH_API_KEY', config('LANGSMITH_API_KEY')
)

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_PROJECT="pr-impassioned-warfare-85"

# Custom Django applications in this project
PROJECT_APPS = [
    'src.accounts',
    'src.chatbot',
    'src.common',
    'src.products',
    'src.shopping_bags',
    'src.wishlists',
    'src.orders',
]

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'cloudinary',
    'cloudinary_storage',
    'django_celery_beat',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
] + PROJECT_APPS

ASGI_APPLICATION = 'src.asgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DRF React Gems',
    'DESCRIPTION': 'E-commerce platform',
    'VERSION': '1.0.0',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

AUTHENTICATION_BACKENDS = [
    # Custom authentication backend
    'src.accounts.authentication.CustomAuthBackendBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', config('DB_NAME')),
        'USER': os.getenv('DB_USER', config('DB_USER')),
        'PASSWORD': os.getenv('DB_PASS', config('DB_PASS')),
        'HOST': os.getenv('DB_HOST', config('DB_HOST')),
        'PORT': os.getenv('DB_PORT', config('DB_PORT')),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # Custom validators
    {
        'NAME': 'src.accounts.validators.password.DigitRequiredValidator',
    },
    {
        'NAME': 'src.accounts.validators.password.UpperCaseLetterRequiredValidator',
    },
    {
        'NAME': 'src.accounts.validators.password.LowerCaseLetterRequiredValidator',
    },
    {
        'NAME': 'src.accounts.validators.password.NoWhiteSpacesRequiredValidator',
    },
    {
        'NAME': 'src.accounts.validators.password.SpecialCharRequiredValidator',
    },
]

AUTH_USER_MODEL = 'accounts.UserCredential'

PASSWORD_RESET_TIMEOUT = 3600

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME', config('CLOUD_NAME')),
    api_key=os.getenv('CLOUD_API_KEY', config('CLOUD_API_KEY')),
    api_secret=os.getenv('CLOUD_API_SECRET', config('CLOUD_API_SECRET')),
)

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', config('CELERY_BROKER_URL'))
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', config('CELERY_RESULT_BACKEND')
)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_POOL_LIMIT = 2
CELERY_RESULT_BACKEND_CONNECTION_RETRY_ON_STARTUP = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = os.getenv('EMAIL_HOST', config('EMAIL_HOST'))
EMAIL_PORT = os.getenv('EMAIL_PORT', config('EMAIL_PORT'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', config('EMAIL_HOST_USER'))
DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL', config('DEFAULT_FROM_EMAIL')
)
SERVER_EMAIL = os.getenv('SERVER_EMAIL', config('SERVER_EMAIL'))
EMAIL_HOST_PASSWORD = os.getenv(
    'EMAIL_HOST_PASSWORD', config('EMAIL_HOST_PASSWORD')
)

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', config('SENTRY_DSN')),
    send_default_pii=True,
)

FRONTEND_URL = os.getenv('FRONTEND_URL', config('FRONTEND_URL'))
