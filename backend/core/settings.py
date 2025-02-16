import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'prompts',
    'packages',
    'avatars',
    'payments',
    'leonardo_service',
    "django_celery_beat",
    "django_celery_results",
    

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "core.middleware.RedirectToAdminMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/admin-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")

# Сколько файлов потребуеттся загрузить для создания аватара
IMAGES_COUNT = int(os.getenv("IMAGES_COUNT", 10))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Celery Configuration Options
CELERY_BROKER_URL = "redis://redis:6379/0"  # URL брокера (Redis)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_RESULT_EXPIRES = 604800
CELERY_TASK_TRACK_STARTED = True  # Отслеживать статус "выполняется"
CELERY_TASK_TIME_LIMIT = 300  # Максимальное время выполнения задачи (в секундах)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND = "redis://redis:6379/0"


#  Юкасса 
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")



CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8080/").split(",")

API_URL = os.getenv("API_URL")
ADMIN_TG = os.getenv("ADMIN_TG")
BOT_TG = os.getenv("BOT_TG")