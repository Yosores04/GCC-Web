from django.db.backends.mysql.features import DatabaseFeatures as MySQLDatabaseFeatures
from django.utils.functional import cached_property


class DatabaseFeatures(MySQLDatabaseFeatures):
    # MariaDB 10.4 doesn't support INSERT ... RETURNING.
    @cached_property
    def can_return_columns_from_insert(self):
        return False
