# Authentication utilities
import hashlib
import sqlite3
from config import SQLITE_DB_PATH

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def authenticate_admin(username: str, password: str) -> bool:
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=? AND role='admin'", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return verify_password(password, row[0])
    return False

def change_admin_password(username: str, current_password: str, new_password: str) -> (bool, str):
    """Change admin password if current password is correct. Returns (success, message)."""
    from db.database_operations import update_admin_password
    if not authenticate_admin(username, current_password):
        return False, "Current password is incorrect."
    new_hashed = hash_password(new_password)
    success = update_admin_password(username, new_hashed)
    if success:
        return True, "Password updated successfully."
    else:
        return False, "Failed to update password. Please try again."
