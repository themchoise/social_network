"""
Configuraciones específicas para producción
Este archivo extiende settings.py con configuraciones optimizadas para CapRover
"""

from .settings import *
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

# Configurar ALLOWED_HOSTS desde variable de entorno o usar localhost
ALLOWED_HOSTS_ENV = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]

# CSRF confiable para CapRover
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='http://localhost:8000,http://127.0.0.1:8000'
)
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS.split(',')]

DATABASE_URL = config('DATABASE_URL', default='sqlite:///app/db.sqlite3')

if DATABASE_URL.startswith('postgres://'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
elif DATABASE_URL.startswith('mysql://'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'error_formatter': {
            'format': '[{asctime}] {levelname} - ERROR ID: {error_id} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_errors.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'application_errors.log',
            'formatter': 'error_formatter',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'error_handler': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# CORS configurado específicamente (no para todos los orígenes)
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True