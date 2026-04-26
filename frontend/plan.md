# Frontend Prototype — Design Plan
**Project:** Voice-Based Transport Enquiry System  
**Phase:** 6 — Front-End & Database Connectivity  
**Scope:** Local prototype only (localhost)  
**Stack:** HTML · CSS · Python Flask · mysql-connector-python · MySQL

---

## 1. Overview

A locally-hosted multi-page HTML prototype that connects to the existing
`transport_enquiry_system` MySQL database. Two distinct portals:

| Portal | Purpose |
|--------|---------|
| **User Portal** | Register/login by email, browse routes, book tickets, view own bookings & enquiries |
| **Admin Portal** | Hardcoded login, view ALL bookings, manage schedules, view payments |

---

## 2. Architecture

```
frontend/
├── plan.md                  ← This file
├── todo.md                  ← Task checklist
├── app.py                   ← Flask server (all routes/API)
├── db.py                    ← MySQL connection helper
├── templates/
│   ├── base.html            ← Shared nav/header shell
│   ├── index.html           ← Landing page (choose User / Admin)
│   │
│   ├── user/
│   │   ├── login.html       ← Email-based user lookup / register
│   │   ├── dashboard.html   ← User home (my bookings, quick actions)
│   │   ├── routes.html      ← Browse available routes & schedules
│   │   ├── book.html        ← Booking form (seat selection + payment)
│   │   ├── bookings.html    ← User's booking history
│   │   └── enquiry.html     ← Submit / view enquiries
│   │
│   └── admin/
│       ├── login.html       ← Admin credential form
│       ├── dashboard.html   ← Stats overview
│       ├── bookings.html    ← All bookings table
│       ├── schedules.html   ← View/add schedules
│       └── payments.html    ← Payment records
│
└── static/
    └── style.css            ← Single shared stylesheet
```

### Data Flow

```
Browser HTML Form
      │  POST/GET
      ▼
Flask app.py  ──── db.py ──── mysql-connector ──── MySQL DB
      │
      ▼ render_template()
  Jinja2 HTML
```

---

## 3. Database Mapping to UI

| UI Action | Tables touched |
|-----------|---------------|
| User register | `USER`, `USER_PHONE` |
| User login (email lookup) | `USER` |
| Browse routes | `ROUTE`, `SCHEDULE`, `TRANSPORT` |
| Make booking | `BOOKING` (INSERT + PAYMENT INSERT) |
| View my bookings | `BOOKING` JOIN `SCHEDULE` JOIN `ROUTE` |
| Submit enquiry | `ENQUIRY` INSERT |
| View enquiries | `ENQUIRY` |
| Admin: all bookings | `BOOKING` JOIN `USER` JOIN `SCHEDULE` JOIN `ROUTE` |
| Admin: schedules | `SCHEDULE` JOIN `ROUTE` JOIN `TRANSPORT` |
| Admin: payments | `PAYMENT` JOIN `BOOKING` JOIN `USER` |

---

## 4. Flask Endpoint Map

### User Routes
| Method | Endpoint | Action |
|--------|----------|--------|
| GET | `/` | Landing page |
| GET/POST | `/user/login` | Email lookup / register |
| GET | `/user/dashboard` | User home |
| GET | `/user/routes` | List routes & schedules |
| GET/POST | `/user/book/<schedule_id>` | Booking form & submit |
| GET | `/user/bookings` | My bookings |
| GET/POST | `/user/enquiry` | Enquiry form & list |

### Admin Routes
| Method | Endpoint | Action |
|--------|----------|--------|
| GET/POST | `/admin/login` | Admin login |
| GET | `/admin/dashboard` | Stats |
| GET | `/admin/bookings` | All bookings |
| GET | `/admin/schedules` | All schedules (+ add form) |
| POST | `/admin/schedules/add` | Insert new schedule |
| GET | `/admin/payments` | Payment records |
| GET | `/admin/logout` | Clear session |

---

## 5. Session Strategy

- Flask `session` (server-side, cookie-based secret key)
- `session['user_id']` → set on user login, cleared on logout
- `session['is_admin']` → set on admin login
- Protected routes check session; redirect to login if missing

---

## 6. Assumptions & Decisions Log

| # | Decision | Alternatives Considered | Reason |
|---|----------|------------------------|--------|
| 1 | Flask as backend | FastAPI, raw CGI | Already in tech stack per README |
| 2 | Email-only user login (no passwords) | Full auth with bcrypt | Prototype only; simplicity wins |
| 3 | Admin credentials hardcoded (`admin` / `admin123`) | DB-based admin table | Prototype only |
| 4 | Jinja2 templates (server-side render) | JS fetch + JSON API | Simpler for pure HTML prototype |
| 5 | Single `style.css` | Per-page CSS | Maintainability for a small project |
| 6 | Seat picker grid — user clicks an available seat | Auto-assign, manual text input | Visual, intuitive for prototype |
| 7 | Cancel booking = DELETE from BOOKING (cascades to PAYMENT) | Status flag | Simpler; schema has ON DELETE CASCADE |
| 8 | Admin full CRUD: Routes, Transports, Schedules, Stations | View-only | User confirmed full management needed |
| 9 | Payment auto-set to "Pending" on booking | Full payment gateway | Prototype only |

---

## 7. Non-Functional Requirements (Prototype Scope)

- **Performance:** Single-user local, no optimization needed
- **Security:** Basic session guard; no SQL injection hardening beyond parameterized queries
- **Reliability:** No uptime requirements; local dev server
- **Scalability:** N/A (prototype)

---

## 8. File Creation Order (Implementation Sequence)

1. `db.py` — DB connection helper
2. `app.py` — Flask skeleton + all routes
3. `static/style.css` — Shared styles
4. `templates/base.html` — Layout shell
5. `templates/index.html` — Landing
6. User portal templates (login → dashboard → routes → book → bookings → enquiry)
7. Admin portal templates (login → dashboard → bookings → schedules → payments)
8. End-to-end test walkthrough

---

## 9. Running Instructions

```bash
# 1. Install dependencies
pip install flask mysql-connector-python

# 2. Import DB schema (if not already done)
mysql -u root -p < ../src/transport_enquiry_system.sql

# 3. Configure DB credentials in db.py

# 4. Run
cd frontend
python app.py

# 5. Open browser
http://localhost:5000
```
