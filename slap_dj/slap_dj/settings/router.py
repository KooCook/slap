from decouple import config

__all__ = ['Router']


class Router:
    """
    A router to control all database operations.
    """

    def db_for_read(self, model, **hints):
        if config('USE_SQLITE_DB', default=False, cast=bool):
            return 'sqlite'
        return 'default'

    def db_for_write(self, model, **hints):
        if config('USE_SQLITE_DB', default=False, cast=bool):
            return 'sqlite'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
