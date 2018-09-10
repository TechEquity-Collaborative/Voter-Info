"""
Django settings for voter_info project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

env = os.environ.copy()
IN_PRODUCTION = os.getenv('ON_HEROKU', False)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if IN_PRODUCTION:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', None)
    DEBUG = False
    RAVEN_CONFIG = {
        # TODO(Eric) Wire up releases
        'dsn': os.getenv('SENTRY_DSN', None),
    }
else:
    DEBUG = True
    SECRET_KEY = '270i7+@=r$sc#1hv!6#lkl6j+fhd8cwvn6$^ijk4q6l#0d&nu1'

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # django framework
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # 3rd party libs
    'rest_framework',
    'raven.contrib.django.raven_compat',
    # handle's production static assets
    'whitenoise.runserver_nostatic',

    # our libs
    'voter_info',
    'districts',
    'offices',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if not IN_PRODUCTION:
    MIDDLEWARE.append('voter_info.middleware.dev_cors_middleware')

ROOT_URLCONF = 'voter_info.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'voter_info.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# Django static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend", "build"),
]
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if IN_PRODUCTION:
    # Configure Django App for Heroku.
    import django_heroku
    django_heroku.settings(locals(), staticfiles=False)
    # for setting up geo-django support with heroku: https://devcenter.heroku.com/articles/postgis
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
else:
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'voter_info_dev',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'USER': 'voter_info_dev_user',
            'PASSWORD': 'super_sekrit_dev_pw_1234',
        }
    }

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')
