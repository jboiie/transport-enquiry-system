# Voice Based Transport Enquiry System

**Course:** 21CSC205P Database Management Systems
**Team Members:** Jai [RA2411026010131], Aggam Singh Arora [RA2411026010139]
**Institution:** SRM Institute of Science and Technology

## 📌 Project Overview
This project is a comprehensive relational database system designed to manage transport-related operations, including user management, route scheduling, ticket bookings, and payment processing. The system strictly adheres to academic DBMS concepts, ensuring robust data integrity, normalization, and concurrency control.

## 🛠️ Tech Stack
* **Database:** MySQL
* **Backend:** Python (Flask)
* **Frontend:** HTML / CSS
* **Connectivity:** `mysql-connector-python`

## 🗄️ Database Schema
The database consists of fully normalized tables (up to 5NF):
* `USER` (user_id, first_name, last_name, email)
* `USER_PHONE` (user_id, phone)
* `ENQUIRY` (user_id, enquiry_number, enquiry_date, status)
* `ROUTE` (route_id, source, destination)
* `SCHEDULE` (schedule_id, route_id)
* `STATION` (station_id, station_name, city)
* `ROUTE_STATION` (route_id, station_id)
* `BOOKING` (booking_id, booking_date, seat_number, user_id, schedule_id, booking_status)
* `PAYMENT` (payment_id, amount, payment_mode, payment_status, booking_id)

## 🚀 Project Implementation Phases

### Phase 1: Conceptual Design (ER Modeling)
* Identified Strong and Weak Entities (e.g., `ENQUIRY` dependent on `USER`).
* Mapped relationships (1:M for User-Booking, M:N for Route-Station).
* Handled multi-valued attributes (User Phones) and composite attributes (Names).

### Phase 2: Logical Schema & Implementation
* Executed Data Definition Language (DDL) to structure the database.
* Enforced constraints (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`).
* Executed Data Manipulation Language (DML) for data seeding.

### Phase 3: Advanced Database Operations
* Implemented **Complex Queries** using Subqueries (`IN`, `EXISTS`) and Set Operations (`UNION`).
* Utilized **Joins** (`INNER`, `LEFT`, `RIGHT`) for multi-table data extraction.
* Created **Views** for restricted data access.
* Developed **Triggers** (e.g., auto-updating audit logs).
* Implemented **Cursors** for row-by-row data processing inside stored procedures.

### Phase 4: Database Normalization (1NF to 5NF)
* **1NF:** Extracted multi-valued phone numbers into `USER_PHONE`.
* **2NF:** Removed partial dependencies by isolating user details from composite keys.
* **3NF:** Removed transitive dependencies by separating `ROUTE` details from `SCHEDULE`.
* **BCNF:** Ensured all determinants were candidate keys.
* **4NF:** Isolated independent multi-valued facts into `ROUTE_STATION` to prevent cross-multiplication.
* **5NF:** Achieved a lossless-join core transaction table in `BOOKING`.

### Phase 5: Transaction & Concurrency Control
* Maintained **ACID Properties** (Atomicity, Consistency, Isolation, Durability).
* Managed transactions using TCL commands (`START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`).
* Implemented **Concurrency Control** using Table-Level and Row-Level Locking (`LOCK TABLES WRITE`, `SELECT ... FOR UPDATE`) to prevent data anomalies during simultaneous bookings.

### Phase 6: Front-End & Database Connectivity
* Designed an HTML interface for user input.
* Built a Flask backend to securely connect to the MySQL database.
* Successfully processed user inputs via POST requests to perform `INSERT` operations into the database.

## ⚙️ How to Run
1. Import the SQL schema using MySQL CLI or Workbench.
2. Ensure Python is installed along with the required libraries (`pip install flask mysql-connector-python`).
3. Update the database credentials in the backend script.
4. Run the server (e.g., `python app.py`).
5. Navigate to the local host port (e.g., `http://localhost:3000`) to interact with the system.
