# Database operations module
# Implement your database helper functions here

import sqlite3
from config import SQLITE_DB_PATH

def get_sqlite_connection():
    import logging
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        return conn
    except Exception as e:
        logging.error(f'Error connecting to SQLite3: {e}')
        return None

# Example usage for SQLite3 (add similar wrappers for CRUD as for MySQL):
def create_sqlite_tables():
    conn = get_sqlite_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        conn.commit()
        cursor.close()
        conn.close()

def create_all_sqlite_tables():
    conn = get_sqlite_connection()
    if conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        # Add more table creation statements as needed for your app
        conn.commit()
        cursor.close()
        conn.close()
        import logging
        logging.info('All SQLite tables ensured.')

def ensure_default_admin():
    from auth.auth_utils import hash_password
    conn = get_sqlite_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", ('admin',))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', hash_password('adminpass'), 'admin')
            )
            conn.commit()
        cursor.close()
        conn.close()
        import logging
        logging.info('Default admin user ensured.')

# Confirm database connection at import/startup
if __name__ == "__main__" or True:
    import logging
    try:
        conn = get_sqlite_connection()
        if conn:
            logging.info('Database connection test: SUCCESS')
            print('Database connection test: SUCCESS')
            conn.close()
        else:
            logging.error('Database connection test: FAILED')
            print('Database connection test: FAILED')
    except Exception as e:
        logging.error(f'Database connection test: ERROR - {e}')
        print(f'Database connection test: ERROR - {e}')

# Ensure tables exist at import/startup
create_all_sqlite_tables()
ensure_default_admin()
