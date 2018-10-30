# See: https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#database-routers


class InspirehepRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api':
            return 'inspirehep'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'api':
            return False
        return None

    # def allow_relation(self, obj1, obj2, **hints):

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'api':
            return False
        return None
