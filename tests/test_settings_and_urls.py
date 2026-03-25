import os
from types import SimpleNamespace
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase

from config import settings as project_settings


class SettingsAndURLTests(SimpleTestCase):
    def test_secret_dashboard_path_defined(self):
        self.assertTrue(hasattr(settings, "SECRET_DASHBOARD_PATH"))
        self.assertTrue(settings.SECRET_DASHBOARD_PATH.endswith("/"))

    def test_default_database_is_sqlite(self):
        with patch.dict(os.environ, {"DB_ENGINE": "sqlite"}, clear=False):
            config = project_settings.build_database_config()
        self.assertEqual(config["ENGINE"], "django.db.backends.sqlite3")
        self.assertIn("db.sqlite3", str(config["NAME"]))

    def test_mysql_database_config_can_be_built_from_env(self):
        env = {
            "DB_ENGINE": "mysql",
            "DB_NAME": "gcc_site",
            "DB_USER": "gcc_user",
            "DB_PASSWORD": "secretpw",
            "DB_HOST": "127.0.0.1",
            "DB_PORT": "3306",
            "DB_ALLOW_LEGACY_MARIADB": "false",
        }
        with patch.dict(os.environ, env, clear=False):
            config = project_settings.build_database_config()

        self.assertEqual(config["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(config["NAME"], "gcc_site")
        self.assertEqual(config["USER"], "gcc_user")
        self.assertEqual(config["PASSWORD"], "secretpw")
        self.assertEqual(config["HOST"], "127.0.0.1")
        self.assertEqual(config["PORT"], "3306")

    def test_mysql_can_use_legacy_mariadb_compat_backend(self):
        env = {
            "DB_ENGINE": "mysql",
            "DB_ALLOW_LEGACY_MARIADB": "true",
        }
        with patch.dict(os.environ, env, clear=False):
            config = project_settings.build_database_config()

        self.assertEqual(config["ENGINE"], "config.db_backends.mysql_legacy")

    def test_legacy_mysql_backend_disables_insert_returning(self):
        from config.db_backends.mysql_legacy.features import DatabaseFeatures

        features = DatabaseFeatures(SimpleNamespace())
        self.assertFalse(features.can_return_columns_from_insert)
        self.assertFalse(features.can_return_rows_from_bulk_insert)
