"""
Development settings.
"""

from .settings_base import *


DEBUG = True
SECRET_KEY = 'secretkey'
AUTH_PASSWORD_VALIDATORS = []
ALLOWED_HOSTS = ['*']

INSPIRE_DATABASE_KEY = 'inspirehep'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inspire-read-api',
        'USER': 'inspire-read-api',
        'PASSWORD': 'Password123',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
    },

    INSPIRE_DATABASE_KEY: {
        'ENGINE': 'django.db.backends.postgresql',
        #'NAME': 'inspire-prod-dump-201804',
        'NAME': 'inspire-prod-dump-20181101',
        'USER': 'inspire-read-api',
        'PASSWORD': 'Password123',
    }
}


# Key used to encrypt ORCID's access tokens.
ORCID_TOKENS_ENCRYPTION_KEY = 'P6jJhYmcKG668InDIG4xSn3khfyGPvqCA9fYn4KFCTtuPgm8lRHsZACfk0RDFpPqkDOl4RhugpLyPUqsakEDmgFv4ru4f3vhE9VjdyCDJQtfzWGDGkyMGFvxFuWaFRhSEtTGwDIzV2criH1hMsmnvyKRBLX7jYFm9Vidn9BXANAWC7iYzkYfEXtEHs8UluGjSgg5bdUnfI6CCb33KKVWLFCxBpKSBFVwMNMOW21CTWwKUZgF6nSQSj8zSYeJHOzS'
