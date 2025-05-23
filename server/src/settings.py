from pathlib import Path
from datetime import timedelta
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f$$t_6jn+jj(my7bgs(sub#^brednrr*fdje+6$(ro%so&yo0_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
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
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=15),
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
        'NAME': 'django_react_ts_gems_db',
        'USER': 'postgres',
        'PASSWORD': 'S@3ana3a',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Inform Django that we replace the default user with a custom one
AUTH_USER_MODEL = 'accounts.UserCredential'

# Inform Django to which url to redirect to after successful login
# LOGIN_REDIRECT_URL = reverse_lazy('')

# Inform Django to which url to redirect to after logout
# LOGOUT_REDIRECT_URL = reverse_lazy('login')


UNFOLD = {
    'SITE_DROPDOWN': [
        {
            'icon': 'diamond',
            'title': _('DRF-React-TS Gems'),
            'link': '/',
        },
    ],
    'THEME': 'light',
    'STYLES': [
        lambda request: static('css/style.css'),
    ],
    'SCRIPTS': [
        lambda request: static('js/script.js'),
    ],
    'SIDEBAR': {
        'navigation': [
            {
                'title': _('Products'),
                'separator': True,
                'items': [
                    {
                        'title': _('Earwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_earwear_changelist'),
                    },
                    {
                        'title': _('Fingerwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_fingerwear_changelist'),
                    },
                    {
                        'title': _('Neckwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_neckwear_changelist'),
                    },
                    {
                        'title': _('Wristwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_wristwear_changelist'),
                    },
                ],
            },
            {
                'title': _('Materials'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('Colors'),
                        'icon': 'Palette',
                        'link': reverse_lazy('admin:products_color_changelist'),
                    },
                    {
                        'title': _('Materials'),
                        'icon': 'Texture',
                        'link': reverse_lazy('admin:products_material_changelist'),
                    },
                    {
                        'title': _('Stone'),
                        'icon': 'Diamond',
                        'link': reverse_lazy('admin:products_stone_changelist'),
                    },
                    {
                        'title': _('Stone by Color'),
                        'icon': 'Diamond',
                        'link': reverse_lazy('admin:products_stonebycolor_changelist'),
                    },
                ],
            },
            {
                'title': _('Design'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('Collections'),
                        'icon': 'Bookmarks',
                        'link': reverse_lazy('admin:products_collection_changelist'),
                    },
                    {
                        'title': _('Reference'),
                        'icon': 'Topic',
                        'link': reverse_lazy('admin:products_reference_changelist'),
                    },
                ],
            },
            {
                'title': _('Sizes'),
                'icon': 'people',
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('Fingerwear'),
                        'icon': 'crop',
                        'link': reverse_lazy('admin:products_fingerwearsize_changelist'),
                    },
                    {
                        'title': _('Neckwear'),
                        'icon': 'crop',
                        'link': reverse_lazy('admin:products_neckwearsize_changelist'),
                    },
                    {
                        'title': _('Wristwear'),
                        'icon': 'crop',
                        'link': reverse_lazy('admin:products_wristwearsize_changelist'),
                    },
                ],
            },
            {
                'title': _('Users & Groups'),
                'icon': 'people',
                'collapsible': True,
                'separator': True,
                'items': [
                    {
                        'title': _('Users'),
                        'icon': 'person',
                        'link': reverse_lazy('admin:accounts_usercredential_changelist'),
                        'permission': lambda request: request.user.is_superuser,
                    },
                    {
                        'title': _('Groups'),
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                        'permission': lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}
