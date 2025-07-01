from pathlib import Path
from datetime import timedelta
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from corsheaders.defaults import default_headers


import cloudinary
import cloudinary.uploader
import cloudinary.api


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--3tgzk2%%qtoj@iz7(-ag90sm&4g&(x+xdy%e4&bn#p6*n)83x'

DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Guest-Id',
]

PROJECT_APPS = [
    'src.accounts',
    'src.products',
    'src.addresses',
    'src.shopping_bags',
    'src.wishlist',
]

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'cloudinary',
    'cloudinary_storage',

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
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=1),
}

MIDDLEWARE = [
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
    'src.accounts.authentication.CustomAuthBackendBackend',
    'django.contrib.auth.backends.ModelBackend',
]

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

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name='dpgvbozrb',
    api_key='356773277236827',
    api_secret='Txaakp6bHutRt-Aw2ocf-dx7aMA'
)


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
                'permission': lambda request: request.user.has_perm('products.view_earwear'),
                'items': [
                    {
                        'title': _('Earwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_earwear_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_earwear'),
                    },
                    {
                        'title': _('Fingerwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_fingerwear_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_fingerwear'),
                    },
                    {
                        'title': _('Neckwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_neckwear_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_neckwear'),
                    },
                    {
                        'title': _('Wristwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy('admin:products_wristwear_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_wristwear'),
                    },
                ],
            },
            {
                'title': _('Reviews'),
                'separator': True,
                'permission': lambda request: request.user.has_perm('products.view_review'),
                'items': [
                    {
                        'title': _('Product Reviews'),
                        'icon': 'star',
                        'link': reverse_lazy('admin:products_review_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_review'),
                    },
                ],
            },
            {
                'title': _('Characteristics'),
                'separator': True,
                'collapsible': True,
                'permission': lambda request: request.user.has_perm('products.view_color'),
                'items': [
                    {
                        'title': _('Colors'),
                        'icon': 'Palette',
                        'link': reverse_lazy('admin:products_color_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_color'),
                    },
                    {
                        'title': _('Metals'),
                        'icon': 'Texture',
                        'link': reverse_lazy('admin:products_metal_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_metal'),
                    },
                    {
                        'title': _('Stone'),
                        'icon': 'Diamond',
                        'link': reverse_lazy('admin:products_stone_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_stone'),
                    },
                    {
                        'title': _('Collections'),
                        'icon': 'Bookmarks',
                        'link': reverse_lazy('admin:products_collection_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_collection'),
                    },
                    {
                        'title': _('Size'),
                        'icon': 'crop',
                        'link': reverse_lazy('admin:products_size_changelist'),
                        'permission': lambda request: request.user.has_perm('products.view_size'),
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
