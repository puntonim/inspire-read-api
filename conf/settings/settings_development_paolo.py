"""
Development settings.
"""

from .settings_base import *


DEBUG = True
SECRET_KEY = 'secretkey'
AUTH_PASSWORD_VALIDATORS = []
ALLOWED_HOSTS = ['*']

INSPIRE_DATABASE_KEY = 'inspire'
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
    # no need -- GRANT CONNECT ON DATABASE "inspirehep-prod-dump" TO "inspire-read-api";
    # no need -- GRANT USAGE ON SCHEMA public TO "inspire-read-api";
    # GRANT SELECT ON ALL TABLES IN SCHEMA public TO "inspire-read-api";
    INSPIRE_DATABASE_KEY: {
        'ENGINE': 'django.db.backends.postgresql',
        #'NAME': 'inspire-prod-dump-201804',
        'NAME': 'inspire-prod-dump-20181101',
        'USER': 'inspire-read-api',
        'PASSWORD': 'Password123',
    }
}


DATABASE_ROUTERS = ['api.db_models.routers.InspirehepRouter',]
ORCID_APP_CONSUMER_KEY = '0000-0001-8607-8906'

MIGRATION_MODULES = {
    'api': 'tests.api.db_models.migrations'}