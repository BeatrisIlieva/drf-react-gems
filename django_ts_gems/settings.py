from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-#3e+5_yj^r==&n+bo3b6o%s4i2882q73ct5c3im6x(9vvy8!n)'

DEBUG = True

ALLOWED_HOSTS = []


PROJECT_APPS = [
    'django_ts_gems.accounts',
    'django_ts_gems.products',
    'django_ts_gems.inventories',
    'django_ts_gems.addresses',
]

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_ts_gems.urls'

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

WSGI_APPLICATION = 'django_ts_gems.wsgi.application'


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
LOGIN_REDIRECT_URL = reverse_lazy('home')

# Inform Django to which url to redirect to after logout
LOGOUT_REDIRECT_URL = reverse_lazy('login')
