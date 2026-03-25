try:
    import pymysql

    pymysql.install_as_MySQLdb()
except Exception:
    # SQLite-only setups should still run without MySQL dependencies installed.
    pass
