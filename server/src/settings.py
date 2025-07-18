"""
Django Settings Configuration for DRF React Gems E-commerce Platform

Key Features:
- JWT Authentication for API security
- CORS configuration for React frontend integration
- Cloudinary for media file storage
- Custom user model 
- PostgreSQL database for data storage
- Custom password validation rules
"""

from pathlib import Path
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from corsheaders.defaults import default_headers

# Import custom Unfold configuration for admin interface customization
from .unfold import UNFOLD

# Cloudinary imports for cloud-based media file storage
# Cloudinary provides CDN capabilities and automatic image optimization
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--3tgzk2%%qtoj@iz7(-ag90sm&4g&(x+xdy%e4&bn#p6*n)83x'

DEBUG = True

ALLOWED_HOSTS = []

# CORS (Cross-Origin Resource Sharing) configuration
# This allows the React frontend to make API calls
# to this Django backend without browser security restrictions
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # React development server
]

# Additional CORS headers that are allowed
# 'Guest-Id' is a custom header for guest user identification
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Guest-Id',  # Custom header for guest user tracking
]

# Custom Django applications in this project
PROJECT_APPS = [
    'src.accounts',
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
] + PROJECT_APPS

# Django REST Framework configuration
REST_FRAMEWORK = {
    # Authentication classes define how users are authenticated
    # JWT (JSON Web Token) authentication is used for stateless API authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Permission classes define default access control
    # IsAuthenticated means all API endpoints require authentication by default
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT (JSON Web Token) configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=1),
}

MIDDLEWARE = [
    # CORS middleware must come first to handle cross-origin requests
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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
        'NAME': 'django_react_gems_db',
        'USER': 'postgres',
        'PASSWORD': 'S@3ana3a',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation rules
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

# Custom user model
AUTH_USER_MODEL = 'accounts.UserCredential'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# This makes Cloudinary the default storage for media files
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary configuration
cloudinary.config(
    cloud_name='dpgvbozrb',
    api_key='356773277236827',
    api_secret='Txaakp6bHutRt-Aw2ocf-dx7aMA'
)

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
