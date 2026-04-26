"""
find_mysql_pass.py — tries common passwords to find your MySQL root credentials
Run from the frontend/ folder:  python find_mysql_pass.py
"""
import mysql.connector

CANDIDATES = ['', 'root', 'password', 'mysql', '1234', '12345', 'admin',
              'toor', 'srm', 'srmsit', 'test', 'Pass@1234', 'Root@1234',
              'MySQL@1234', 'root123', 'password123']

print("Trying common passwords for root@localhost …\n")
for pw in CANDIDATES:
    try:
        c = mysql.connector.connect(host='localhost', user='root',
                                    password=pw, database='mysql')
        c.close()
        label = repr(pw) if pw else '""  (empty — no password)'
        print(f"✅  FOUND!  Password is: {label}")
        print(f"\n    Open frontend/config.py and set:\n    DB_PASSWORD = {repr(pw)}\n")
        break
    except mysql.connector.Error:
        label = repr(pw) if pw else '""'
        print(f"✗   {label}")
else:
    print("\n❌  None of the common passwords worked.")
    print("    Try one of these options:\n")
    print("    Option A — Reset root password:")
    print("      1. Stop MySQL service:  net stop MySQL  (or MySQL80/MySQL57)")
    print("      2. Start mysqld with skip-grant: mysqld --skip-grant-tables --shared-memory")
    print("      3. Open another terminal: mysql -u root")
    print("      4. Run: FLUSH PRIVILEGES;")
    print("         Then: ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';")
    print("      5. Restart MySQL normally and set DB_PASSWORD = 'newpassword' in config.py\n")
    print("    Option B — Use MySQL Workbench → right-click connection → Edit → copy the password\n")
    print("    Option C — Check your MySQL installer notes or any .env / my.cnf files\n")
