""" Django settings for demetrius project.
"""
import os

from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DEMETRIUS_SECRET_KEY")

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 4

DEBUG = True

ALLOWED_HOSTS = [
    'github.com',
    'jesulayomy.pythonanywhere.com',
    'pythonanywhere.com',
    'vercel.app',
    'nuesafunaab.com.ng',
    '127.0.0.1',
    '0.0.0.0',
    '*'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library.apps.LibraryConfig',
    'rest_framework',
    'corsheaders',
    'django_json_widget',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'demetrius.urls'

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

WSGI_APPLICATION = 'demetrius.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('DB_DEMETRIUS_HOST'),
        'NAME': os.getenv('DB_DEMETRIUS_NAME'),
        'USER': os.getenv('DB_DEMETRIUS_USER'),
        'PASSWORD': os.getenv('DB_DEMETRIUS_PASSWORD'),
    }
}


# Password validation
VALID = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{VALID}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{VALID}.MinimumLengthValidator',
    },
    {
        'NAME': f'{VALID}.CommonPasswordValidator',
    },
    {
        'NAME': f'{VALID}.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
