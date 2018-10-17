"""
Development settings.
"""

from .settings_base import *


DEBUG = True
AUTH_PASSWORD_VALIDATORS = []
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inspire-read-api',
        'USER': 'inspire-read-api',
        'PASSWORD': 'Password123',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
    },

    # To grant read permission to the inspirehep Postgres db:
    # GRANT CONNECT ON DATABASE "inspirehep-prod-dump" TO "inspire-read-api";
    # GRANT USAGE ON SCHEMA public TO "inspire-read-api";
    # GRANT SELECT ON ALL TABLES IN SCHEMA public TO "inspire-read-api";
    'inspirehep': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inspirehep-prod-dump',
        'USER': 'inspire-read-api',
        'PASSWORD': 'Password123',
    }

}


DATABASE_ROUTERS = ['api.dbmodels.routers.InspirehepRouter',]