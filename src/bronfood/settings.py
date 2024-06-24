import os

from pathlib import Path

from celery.schedules import crontab

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ENV_NAME = os.getenv('ENV_NAME', 'local')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'corsheaders',
    'bronfood.core.client.apps.ClientConfig',
    'bronfood.core.useraccount.apps.UseraccountConfig',
    'bronfood.api.apps.ApiConfig',
    'bronfood.core.restaurants',
    'bronfood.core.phone.apps.PhoneConfig',
    'bronfood.core.restaurant_owner.apps.RestaurantOwnerConfig',
    'bronfood.core.restaurant_admin.apps.RestaurantAdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',  # Token
    'djoser',  # Token
    'management_commands.apps.ManagementCommandsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bronfood.urls'

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

WSGI_APPLICATION = 'bronfood.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', 5432)
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'useraccount.UserAccount'

VENDORS = {
    'SMS_BACKENDS': {
        'KAZINFOTECH': {
                'USERNAME': os.getenv('KAZINFOTECH_USERNAME'),
                'PASSWORD': os.getenv('KAZINFOTECH_PASSWORD'),
                'URL': 'https://kazinfoteh.org:9507/api?',
                'ORIGINATOR': 'INFO_KAZ'
            }
        }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# NOTE ТОЛЬКО В РАЗРАБОТКЕ!
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1',
                        'https://127.0.0.1',
                        'http://bronfood.sytes.net',
                        'https://bronfood.sytes.net',
                        'http://www.bronfood.sytes.net',
                        'https://www.bronfood.sytes.net']

AUTHENTICATION_BACKENDS = [
    'bronfood.core.auth_backends.PhoneBackend',
    'bronfood.core.auth_backends.UsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CELERY_BEAT_SCHEDULE = {
    'check_expired_otps_every_minute': {
        'task': 'bronfood.core.phone.tasks.check_expired_otps',
        'schedule': crontab(),
    },
}
