from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper

from .features import DatabaseFeatures


class DatabaseWrapper(MySQLDatabaseWrapper):
    # Local compatibility shim: allows XAMPP MariaDB 10.4 for development.
    features_class = DatabaseFeatures

    def check_database_version_supported(self):
        return
