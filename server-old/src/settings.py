from datetime import timedelta
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-#3e+5_yj^r==&n+bo3b6o%s4i2882q73ct5c3im6x(9vvy8!n)'

DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]


PROJECT_APPS = [
    'src.accounts',
    'src.products',
    'src.addresses',
]

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # pip install django-restframework
    'rest_framework',  
    # pip install djangorestframework-simplejwt
    'rest_framework_simplejwt',  
    # pip install drf-spectacular (swagger)
    'drf_spectacular',  
    # we do not install `token_blacklist`
    # we just add it to installed apps
    # so the blacklisting of the refresh token
    # can happen
    'rest_framework_simplejwt.token_blacklist',  
    # pip install django-cors-headers
    'corsheaders',

] + PROJECT_APPS

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # this setting says that, except explicitly specified,
    # all views will expect the user to be authenticated
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # for swagger
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django App',
    'DESCRIPTION': 'Online store',
    'VERSION': '1.0.0',
}

MIDDLEWARE = [
    # middleware that checks if the Client that sends the request is allowed to
    # this is done through a preflight request with a method `OPTIONS`
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_ts_gems_db',
        'USER': 'postgres',
        'PASSWORD': 'S@3ana3a',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


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

# Inform Django that we replace the default user with a custom one
AUTH_USER_MODEL = 'accounts.UserCredential'

# Inform Django to which url to redirect to after successful login
# LOGIN_REDIRECT_URL = reverse_lazy('home')

# Inform Django to which url to redirect to after logout
# LOGOUT_REDIRECT_URL = reverse_lazy('login')
