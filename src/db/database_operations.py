# Database CRUD and business logic for all tables

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
        # Performance Data table
        cursor.execute('''CREATE TABLE IF NOT EXISTS performance_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            associate_id TEXT NOT NULL,
            associate_name TEXT NOT NULL,
            alliance_type TEXT NOT NULL,
            business_unit TEXT NOT NULL,
            geo TEXT NOT NULL,
            certification_name TEXT NOT NULL,
            completion_date TEXT NOT NULL,
            feedback TEXT,
            activity_code TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        # Global Metrics table
        cursor.execute('''CREATE TABLE IF NOT EXISTS global_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            value REAL NOT NULL,
            geo TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        # BU Metrics table
        cursor.execute('''CREATE TABLE IF NOT EXISTS bu_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_unit TEXT NOT NULL,
            target INTEGER NOT NULL,
            completed INTEGER NOT NULL,
            achievement_percent REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        # Alliance Metrics table
        cursor.execute('''CREATE TABLE IF NOT EXISTS alliance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_name TEXT NOT NULL,
            business_unit TEXT,
            target INTEGER,
            completed INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        # Cost Savings table
        cursor.execute('''CREATE TABLE IF NOT EXISTS cost_savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_name TEXT NOT NULL,
            enablement_saving REAL,
            certification_saving REAL,
            total REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
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

def update_admin_password(username: str, new_hashed_password: str) -> bool:
    """Update the admin's password. Returns True if successful, False otherwise."""
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE username=? AND role='admin'", (new_hashed_password, username))
            conn.commit()
            updated = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return updated
        except Exception as e:
            import logging
            logging.error(f'Error updating admin password: {e}')
            return False
    return False

# CRUD for performance_data
def get_all_performance_data():
    conn = get_sqlite_connection()
    if conn:
        try:
            df = None
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM performance_data", conn)
            conn.close()
            return df
        except Exception as e:
            import logging
            logging.error(f'Error fetching performance data: {e}')
            return None
    return None

def add_performance_record(data: dict) -> tuple[bool, str]:
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO performance_data (associate_id, associate_name, alliance_type, business_unit, geo, certification_name, completion_date, feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['associate_id'], data['associate_name'], data['alliance_type'], data['business_unit'], data['geo'],
                data['certification_name'], data['completion_date'], data.get('feedback', None)
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Record added successfully."
        except Exception as e:
            import logging
            logging.error(f'Error adding performance record: {e}')
            return False, str(e)
    return False, "Database connection failed."

def update_performance_record(record_id: int, data: dict) -> tuple[bool, str]:
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE performance_data SET associate_id=?, associate_name=?, alliance_type=?, business_unit=?, geo=?, certification_name=?, completion_date=?, feedback=?
                WHERE id=?
            """, (
                data['associate_id'], data['associate_name'], data['alliance_type'], data['business_unit'], data['geo'],
                data['certification_name'], data['completion_date'], data.get('feedback', None), record_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Record updated successfully."
        except Exception as e:
            import logging
            logging.error(f'Error updating performance record: {e}')
            return False, str(e)
    return False, "Database connection failed."

def delete_performance_record(record_id: int) -> tuple[bool, str]:
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM performance_data WHERE id=?", (record_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Record deleted successfully."
        except Exception as e:
            import logging
            logging.error(f'Error deleting performance record: {e}')
            return False, str(e)
    return False, "Database connection failed."

# CRUD for global_metrics
def get_all_global_metrics():
    conn = get_sqlite_connection()
    if conn:
        try:
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM global_metrics", conn)
            conn.close()
            return df
        except Exception as e:
            import logging
            logging.error(f'Error fetching global metrics: {e}')
            return None
    return None

def overwrite_global_metrics(df: 'pd.DataFrame') -> (bool, str):
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM global_metrics")
            for _, row in df.iterrows():
                cursor.execute("INSERT INTO global_metrics (metric_name, value, geo) VALUES (?, ?, ?)",
                               (row['metric_name'], row['value'], row.get('geo', None)))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Global metrics updated."
        except Exception as e:
            import logging
            logging.error(f'Error updating global metrics: {e}')
            return False, str(e)
    return False, "Database connection failed."

# CRUD for bu_metrics
def get_all_bu_metrics():
    conn = get_sqlite_connection()
    if conn:
        try:
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM bu_metrics", conn)
            conn.close()
            return df
        except Exception as e:
            import logging
            logging.error(f'Error fetching BU metrics: {e}')
            return None
    return None

def overwrite_bu_metrics(df: 'pd.DataFrame') -> (bool, str):
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bu_metrics")
            for _, row in df.iterrows():
                cursor.execute("INSERT INTO bu_metrics (business_unit, target, completed, achievement_percent) VALUES (?, ?, ?, ?)",
                               (row['business_unit'], row['target'], row['completed'], row.get('achievement_percent', None)))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "BU metrics updated."
        except Exception as e:
            import logging
            logging.error(f'Error updating BU metrics: {e}')
            return False, str(e)
    return False, "Database connection failed."

# CRUD for alliance_metrics
def get_all_alliance_metrics():
    conn = get_sqlite_connection()
    if conn:
        try:
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM alliance_metrics", conn)
            conn.close()
            return df
        except Exception as e:
            import logging
            logging.error(f'Error fetching alliance metrics: {e}')
            return None
    return None

def overwrite_alliance_metrics(df: 'pd.DataFrame') -> (bool, str):
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alliance_metrics")
            for _, row in df.iterrows():
                cursor.execute("INSERT INTO alliance_metrics (partner_name, business_unit, target, completed) VALUES (?, ?, ?, ?)",
                               (row['partner_name'], row.get('business_unit', None), row.get('target', None), row.get('completed', None)))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Alliance metrics updated."
        except Exception as e:
            import logging
            logging.error(f'Error updating alliance metrics: {e}')
            return False, str(e)
    return False, "Database connection failed."

# CRUD for cost_savings
def get_all_cost_savings():
    conn = get_sqlite_connection()
    if conn:
        try:
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM cost_savings", conn)
            conn.close()
            return df
        except Exception as e:
            import logging
            logging.error(f'Error fetching cost savings: {e}')
            return None
    return None

def overwrite_cost_savings(df: 'pd.DataFrame') -> (bool, str):
    conn = get_sqlite_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cost_savings")
            for _, row in df.iterrows():
                cursor.execute("INSERT INTO cost_savings (partner_name, enablement_saving, certification_saving, total) VALUES (?, ?, ?, ?)",
                               (row['partner_name'], row.get('enablement_saving', None), row.get('certification_saving', None), row.get('total', None)))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Cost savings updated."
        except Exception as e:
            import logging
            logging.error(f'Error updating cost savings: {e}')
            return False, str(e)
    return False, "Database connection failed."

# Utility: Validate and standardize date, number fields for upload
def clean_date(date_val):
    from dateutil import parser
    try:
        return parser.parse(str(date_val)).strftime('%Y-%m-%d')
    except Exception:
        return None

def clean_number(num_val):
    import re
    try:
        if isinstance(num_val, (int, float)):
            return float(num_val)
        s = str(num_val).replace(',', '').replace('$', '').replace('₹', '')
        s = re.sub(r'[^0-9.\-]', '', s)
        return float(s)
    except Exception:
        return None
