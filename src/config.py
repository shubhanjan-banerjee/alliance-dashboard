import os

# Database configuration
DB_CONFIG = {
    'host': 'your_mysql_host',
    'database': 'global_alliances_db',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password'
}

# SQLite3 configuration
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'global_alliances_db.sqlite3')
