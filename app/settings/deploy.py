import os
import dj_database_url
from .base import *

DEBUG = False
SITE_DOMAIN = 'http://app.translrrr.gtszoffice.com'
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'translrrr.gtszoffice.com',
    'app.translrrr.gtszoffice.com'
]
DATABASES['default'] = dj_database_url.config(conn_max_age=600)  # noqa: F405
CORS_ORIGIN_WHITELIST = [
    'http://app.translrrr.gtszoffice.com',
    'http://translrrr.gtszoffice.com'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log')
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
