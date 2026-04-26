"""
seed_mock.py — Insert two mock users for quick prototyping
============================================================
Run once from the frontend/ folder:
    python seed_mock.py

Mock login emails (use on the User Portal login page):
    jai@test.com
    aggam@test.com
"""
import sys
from db import get_db

MOCK_USERS = [
    {
        'first_name': 'Jai',
        'last_name': 'Tester',
        'email': 'jai@test.com',
        'phone': '9999900001',
    },
    {
        'first_name': 'Aggam',
        'last_name': 'Tester',
        'email': 'aggam@test.com',
        'phone': '9999900002',
    },
]

def seed():
    try:
        conn = get_db()
    except Exception as e:
        print(f"\n❌  Could not connect to MySQL: {e}")
        print("    → Open frontend/config.py and set DB_PASSWORD to your MySQL root password.\n")
        sys.exit(1)

    cur = conn.cursor(dictionary=True)
    created = 0

    for u in MOCK_USERS:
        cur.execute("SELECT user_id FROM USER WHERE email = %s", (u['email'],))
        row = cur.fetchone()
        if row:
            print(f"✓  {u['email']} already exists (user_id={row['user_id']})")
            continue
        cur.execute(
            "INSERT INTO USER (first_name, last_name, email) VALUES (%s, %s, %s)",
            (u['first_name'], u['last_name'], u['email']))
        uid = cur.lastrowid
        cur.execute(
            "INSERT INTO USER_PHONE (user_id, phone) VALUES (%s, %s)",
            (uid, u['phone']))
        conn.commit()
        print(f"✅  Created user: {u['first_name']} {u['last_name']} | {u['email']} (user_id={uid})")
        created += 1

    cur.close()
    conn.close()
    print(f"\nDone. {created} new user(s) created.")
    print("\n── Mock Login Credentials ─────────────────────────")
    print("  User 1 email : jai@test.com")
    print("  User 2 email : aggam@test.com")
    print("  Admin login  : admin / admin123")
    print("────────────────────────────────────────────────────\n")

if __name__ == '__main__':
    seed()
