"""
Django settings for treat_min project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

ALLOWED_HOSTS = ['treat-min.com', 'www.treat-min.com']
# ALLOWED_HOSTS = []

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'knox',
    'rest_framework',
    'treat_min.accounts.apps.AccountsConfig',
    'treat_min.entities.apps.EntitiesConfig',
    'treat_min.entities_details.apps.EntitiesDetailsConfig',
    'treat_min.user_appointments.apps.UserAppointmentsConfig',
    'treat_min.user_reviews.apps.UserReviewsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['knox.auth.TokenAuthentication']
}

REST_KNOX = {
    # 'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    # 'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(weeks=26),
    # 'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    # 'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': True,
    # 'MIN_REFRESH_INTERVAL': timedelta(hours=1),
    # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'treat_min.urls'

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

WSGI_APPLICATION = 'treat_min.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

AUTH_USER_MODEL = 'accounts.AbstractUser'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]

MULTILINGUAL_LANGUAGES = [
    "en-us",
    "ar-eg",
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Email settings
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@treat-min.com'
with open(os.path.join(BASE_DIR, 'email_password.txt')) as f:
    EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# # HTTPS settings
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# # HSTS settings
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
