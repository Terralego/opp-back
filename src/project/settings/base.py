"""
Django settings
"""

import os
from datetime import timedelta

from django.utils.log import DEFAULT_LOGGING
from terra_utils.helpers import Choices

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(PROJECT_DIR)), 'public')

SECRET_KEY = os.environ.get('SECRET_KEY', 'secretkey-superhot-12345678')

# Installed apps
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_gis',
    'drf_yasg',
    'versatileimagefield',
)

SITE_ID = 1

CUSTOM_APPS = (
    'project',
    'geostore',
    'terra_utils',
    'terra_accounts',
    'datastore',
    'terra_opp',
)

INSTALLED_APPS += CUSTOM_APPS

# Main settings
AUTH_USER_MODEL = 'terra_accounts.TerraUser'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

ROOT_URLCONF = 'project.urls'

LOGGING = DEFAULT_LOGGING

# DRF-related
REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'terra_utils.pagination.PagePagination',
    'PAGE_SIZE': 100,

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_ALLOW_REFRESH': True,
}

SERIALIZATION_MODULES = {
    'geojson': 'geostore.serializers.geojson',
}

# Internationalization
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locales'),
)
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.getenv('TZ', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
STATIC_URL = '/static_dj/'
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Terralego settings
TROPP_STATES = Choices(
    ('DRAFT', 100, 'Draft'),
    ('SUBMITTED', 200, 'Submitted'),
    ('ACCEPTED', 300, 'Accepted'),
    ('REFUSED', -1, 'Refused'),
    ('CANCELLED', -100, 'Cancelled'),
    ('MISSING', 0, 'Missing'),
)
TROPP_STATES.add_subset('MANUAL', (
    'DRAFT',
    'SUBMITTED',
    'ACCEPTED',
    'REFUSED',
    'CANCELLED',
))

IGN = {
    "version": 8,
    "sources": {
        "ign-orthophoto": {
            "type": "raster",
            "tiles": [
                "https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image/jpeg&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}"
            ],
            "minzoom": 0,
            "maxzoom": 22
        }
    },
    "sprite": "https://openmaptiles.github.io/klokantech-basic-gl-style/sprite",
    "glyphs": "mapbox://fonts/makinacorpus/{fontstack}/{range}.pbf",
    "layers": [
        {"id": "ign-orthophoto-background", "type": "raster", "source": "ign-orthophoto"}
    ]
}

TERRA_APPLIANCE_SETTINGS = {
    "map": {
        "accessToken": os.environ.get('MAPBOX_GL_ACCESS_TOKEN'),
        "center": [0, 0],
        "zoom": 4,
        "maxBounds": [[-180, -90], [180, 90]],
        "backgroundStyle": [
            {"label": "Plan", "url": "mapbox://styles/mapbox/streets-v9"},
            {"label": "Orthophoto IGN", "url": IGN},
        ],
    },
    'enabled_modules': ['OPP'],
}

TROPP_VIEWPOINT_PROPERTIES_SET = {
    'pdf': {
        ('site', 'Site'),
        ('voie', 'Voie'),
        ('commune', 'Commune'),
    },
    'form': {},
    'filter': {},
}

TERRA_USER_STRING_FORMAT = 'project.utils.user_string_format'

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'terra_opp': [
        ('original', 'url'),
        ('full', 'thumbnail__1500x1125'),
        ('list', 'thumbnail__300x225'),
        ('thumbnail', 'thumbnail__180x120'),
    ]
}

MIN_TILE_ZOOM = 5
MAX_TILE_ZOOM = 23

TILE_FLAVOR = 'smart'

# Mail
EMAIL_HOST = 'mailcatcher'
EMAIL_PORT = 1025

SWAGGER_ENABLED = False

TROPP_OBSERVATORY_LAYER_PK = 1
