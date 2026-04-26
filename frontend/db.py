"""
db.py — MySQL connection helper
================================
UPDATE the DB_CONFIG block below with your local MySQL credentials
before running the app.
"""
import mysql.connector

# ─── UPDATE THESE ──────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',          # <── your MySQL root password
    'database': 'transport_enquiry_system',
    'autocommit': False,
}
# ───────────────────────────────────────────────────────────────


def get_db():
    """Return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)
