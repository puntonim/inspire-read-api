# See: https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#database-routers

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import connection


class InspirehepRouter:
    def db_for_read(self, model, **hints):
        """
        Return the key in settings.DATABASES to be used in read ops.
        """
        if model._meta.app_label == 'api':
            # Tests write to te default db, so if we are running tests (detected
            # because of the db name), then provide no suggestion.
            if connection.settings_dict['NAME'].startswith('test_'):
                return None
            return settings.INSPIRE_DATABASE_KEY
        return None  # It means no suggestion, thus to go on asking the regular Router.

    def db_for_write(self, model, **hints):
        """
        Return the key in settings.DATABASES to be used in write ops.
        """
        if model._meta.app_label == 'api':
            # Note: models with managed = False are ignored during `migrate` and
            # `makemigrations`. But they are writable by a: Model.objets.create().
            # To make them read only, this is the right place.
            raise PermissionDenied(
                'All models in the "api" apps are unmanaged and read-only')
        return None  # It means no suggestion, thus to go on asking the regular Router.

    # def allow_relation(self, obj1, obj2, **hints):

    # def allow_migrate(self, db, app_label, model_name=None, **hints):
