"""
Django Settings Configuration for DRF React Gems E-commerce Platform

This file contains all the configuration settings for the Django project.
It defines database connections, installed apps, middleware, authentication,
and other essential Django settings for the e-commerce application.

Key Features:
- JWT Authentication for API security
- CORS configuration for React frontend integration
- Cloudinary for media file storage
- Custom user model for enhanced user management
- PostgreSQL database for robust data storage
- Custom password validation rules
"""

# Standard library imports for path handling and time calculations
from pathlib import Path
from datetime import timedelta

# Django utilities for internationalization and CORS headers
from django.utils.translation import gettext_lazy as _
from corsheaders.defaults import default_headers

# Import custom Unfold configuration for admin interface customization
from .unfold import UNFOLD

# Cloudinary imports for cloud-based media file storage
# Cloudinary provides CDN capabilities and automatic image optimization
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This creates an absolute path to the project root directory
# Path(__file__) gets the current file's path, .resolve() resolves any symlinks,
# .parent.parent goes up two levels: from src/settings.py to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing and should be kept secure
# In production, this should be stored as an environment variable
SECRET_KEY = 'django-insecure--3tgzk2%%qtoj@iz7(-ag90sm&4g&(x+xdy%e4&bn#p6*n)83x'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True enables detailed error pages and development features
# Set to False in production for security
DEBUG = True

# ALLOWED_HOSTS defines which hostnames can serve this Django application
# In production, add your real domain names here.
# 'testserver' is required for Django's test client to work:
#   - When you run tests (python manage.py test or pytest), Django uses 'testserver' as the HTTP_HOST.
#   - If 'testserver' is not in this list, tests that make requests will fail with an Invalid HTTP_HOST error.
#   - This does NOT affect production or real users—only automated tests use 'testserver'.
#   - It is safe to keep 'testserver' here in all environments.
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',  # Required for Django test client; see note above
]

# CORS (Cross-Origin Resource Sharing) configuration
# This allows the React frontend (running on localhost:5173) to make API calls
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
# These are the apps that contain our business logic
PROJECT_APPS = [
    'src.accounts',      # User authentication and profile management
    'src.common',        # Shared utilities and common functionality
    'src.products',      # Product catalog and inventory management
    'src.shopping_bags', # Shopping cart functionality
    'src.wishlists',     # User wishlist management
    'src.orders',        # Order processing and management
]

# INSTALLED_APPS defines all Django applications that are enabled
# Django will look for models, admin, and other components in these apps
INSTALLED_APPS = [
    # Unfold - Custom Django admin interface for better UX
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    # Cloudinary - Cloud-based media file storage
    'cloudinary',
    'cloudinary_storage',

    # Django's built-in applications
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # Authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Message framework
    'django.contrib.staticfiles',  # Static file serving

    # Third-party applications
    'rest_framework',              # Django REST Framework for API building
    'rest_framework_simplejwt',    # JWT authentication for DRF
    'rest_framework_simplejwt.token_blacklist',  # Token blacklisting for security
    'corsheaders',                 # CORS handling for cross-origin requests
] + PROJECT_APPS  # Add our custom applications

# Django REST Framework configuration
# This defines how API requests are handled and authenticated
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
# JWT tokens are used for stateless authentication between frontend and backend
SIMPLE_JWT = {
    # Access tokens are short-lived for security (15 minutes)
    # They are used for API access and should be refreshed frequently
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    # Refresh tokens are long-lived (1 day) and used to get new access tokens
    # They allow users to stay logged in without re-entering credentials
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# MIDDLEWARE defines the order of middleware classes that process requests
# Middleware are functions that run on every request/response
MIDDLEWARE = [
    # CORS middleware must come first to handle cross-origin requests
    'corsheaders.middleware.CorsMiddleware',

    # Django's built-in middleware (in recommended order)
    'django.middleware.security.SecurityMiddleware',      # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling
    'django.middleware.common.CommonMiddleware',         # URL routing
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
]

# URL configuration - tells Django where to find the main URL patterns
ROOT_URLCONF = 'src.urls'

# Template configuration for rendering HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'  # Additional template directories
        ],
        'APP_DIRS': True,  # Look for templates in each app's templates/ directory
        'OPTIONS': {
            'context_processors': [
                # Context processors add variables to all templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application entry point for deployment
WSGI_APPLICATION = 'src.wsgi.application'

# Authentication backends define how users are authenticated
# Multiple backends can be used, Django tries them in order
AUTHENTICATION_BACKENDS = [
    # Custom authentication backend for enhanced user management
    'src.accounts.authentication.CustomAuthBackendBackend',
    # Django's default authentication backend
    'django.contrib.auth.backends.ModelBackend',
]

# Database configuration
# PostgreSQL is used for its robustness and advanced features
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL database engine
        'NAME': 'django_react_gems_db',             # Database name
        'USER': 'postgres',                         # Database user
        'PASSWORD': 'S@3ana3a',                     # Database password
        'HOST': '127.0.0.1',                       # Database host (localhost)
        'PORT': '5432',                             # PostgreSQL default port
    }
}

# Password validation rules
# These ensure users create strong, secure passwords
AUTH_PASSWORD_VALIDATORS = [
    # Check if password is too similar to user's other personal information
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Ensure password meets minimum length requirement
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    # Check against common password list
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # Ensure password is not entirely numeric
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # Custom validators for enhanced security
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
# This replaces Django's default User model with our custom implementation
# Allows us to add custom fields and methods to the user model
AUTH_USER_MODEL = 'accounts.UserCredential'

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'        # Timezone for the application
USE_I18N = True          # Enable internationalization
USE_TZ = True            # Enable timezone support

# Static files configuration
# Static files are CSS, JavaScript, images that don't change
STATIC_URL = 'static/'  # URL prefix for static files
STATICFILES_DIRS = (
    BASE_DIR / 'static',  # Additional directories for static files
)

# Media files configuration
# Media files are user-uploaded content like images
MEDIA_URL = 'media/'  # URL prefix for media files
MEDIA_ROOT = BASE_DIR / 'mediafiles/'  # Directory where media files are stored

# Default primary key field type
# BigAutoField provides larger range than AutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary storage configuration
# This makes Cloudinary the default storage for media files
# Files uploaded through Django will be stored in the cloud
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary configuration
# These credentials connect Django to your Cloudinary account
# In production, these should be environment variables
cloudinary.config(
    cloud_name='dpgvbozrb',      # Your Cloudinary cloud name
    api_key='356773277236827',    # Your Cloudinary API key
    api_secret='Txaakp6bHutRt-Aw2ocf-dx7aMA'  # Your Cloudinary API secret
)
