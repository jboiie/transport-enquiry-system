"""
db.py — MySQL connection helper
================================
Set your MySQL password in frontend/config.py (that file is gitignored).

Create frontend/config.py with:
    DB_PASSWORD = "your_actual_password_here"
"""
import mysql.connector

# Try to load password from local config.py (gitignored, never committed)
try:
    from config import DB_PASSWORD
except ImportError:
    DB_PASSWORD = ''   # fallback — set password in config.py!

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': DB_PASSWORD,
    'database': 'transport_enquiry_system',
    'autocommit': False,
}


def get_db():
    """Return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)

