"""
migrate_db.py — Adds the `enquiry_text` column to the ENQUIRY table.
Run from the frontend/ folder once you have your DB_PASSWORD correctly set in config.py:
    python migrate_db.py
"""
import sys
from db import get_db

def migrate():
    try:
        conn = get_db()
    except Exception as e:
        print(f"\n❌ Could not connect to MySQL: {e}")
        print("   Make sure frontend/config.py has the correct DB_PASSWORD.\n")
        sys.exit(1)

    cur = conn.cursor()
    try:
        print("Checking ENQUIRY table structure...")
        cur.execute("SHOW COLUMNS FROM ENQUIRY LIKE 'enquiry_text'")
        result = cur.fetchone()
        
        if result:
            print("✅ 'enquiry_text' column already exists. No migration needed.")
        else:
            print("Adding 'enquiry_text' column to ENQUIRY table...")
            cur.execute("ALTER TABLE ENQUIRY ADD COLUMN enquiry_text TEXT")
            conn.commit()
            print("✅ Migration successful!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    migrate()
