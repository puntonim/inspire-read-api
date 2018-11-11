"""
Production settings.
"""

from .settings_base import *


DEBUG = False
ALLOWED_HOSTS = ['mysite.com']
SECRET_KEY = 'mysecretkey'
ORCID_TOKENS_ENCRYPTION_KEY = 'mykey'