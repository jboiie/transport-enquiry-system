# Frontend Prototype — Task Checklist

> Track progress here. Mark `[x]` when done, `[/]` when in progress.

---

## Phase A — Foundation

- [ ] Create `frontend/` folder structure (templates/, static/)
- [ ] Write `db.py` — MySQL connection helper with config block
- [ ] Write `app.py` — Flask app skeleton, session config, all route stubs

---

## Phase B — Shared UI

- [ ] Create `static/style.css` — base reset, nav, tables, forms, buttons
- [ ] Create `templates/base.html` — nav bar (User | Admin links), flash messages
- [ ] Create `templates/index.html` — landing page with two portal cards

---

## Phase C — User Portal

- [ ] `templates/user/login.html` — email input, register form
- [ ] Flask: `GET/POST /user/login` — lookup USER by email; register if not found
- [ ] `templates/user/dashboard.html` — welcome + quick stats (booking count)
- [ ] Flask: `GET /user/dashboard` — fetch user summary from DB
- [ ] `templates/user/routes.html` — table of ROUTE + SCHEDULE + TRANSPORT
- [ ] Flask: `GET /user/routes` — query all upcoming schedules with route info
- [ ] `templates/user/book.html` — schedule detail + seat + payment mode form
- [ ] Flask: `POST /user/book/<schedule_id>` — INSERT BOOKING then INSERT PAYMENT
- [ ] `templates/user/bookings.html` — table of user's bookings + payment status
- [ ] Flask: `GET /user/bookings` — JOIN BOOKING, SCHEDULE, ROUTE, PAYMENT
- [ ] `templates/user/enquiry.html` — submit form + list of past enquiries
- [ ] Flask: `GET/POST /user/enquiry` — INSERT ENQUIRY + SELECT ENQUIRY for user

---

## Phase D — Admin Portal

- [ ] `templates/admin/login.html` — username/password form
- [ ] Flask: `GET/POST /admin/login` — hardcoded credential check, set session
- [ ] `templates/admin/dashboard.html` — stat cards (total users, bookings, revenue)
- [ ] Flask: `GET /admin/dashboard` — aggregate queries
- [ ] `templates/admin/bookings.html` — all bookings table (user + route + seat + status)
- [ ] Flask: `GET /admin/bookings` — full JOIN query
- [ ] `templates/admin/schedules.html` — all schedules + add-schedule form
- [ ] Flask: `GET /admin/schedules` + `POST /admin/schedules/add`
- [ ] `templates/admin/payments.html` — all payments with booking & user info
- [ ] Flask: `GET /admin/payments` — JOIN PAYMENT, BOOKING, USER
- [ ] Flask: `GET /admin/logout` — clear session, redirect to index

---

## Phase E — Polish & Verification

- [ ] Add session guards (redirect if not logged in) to all protected routes
- [ ] Add flash messages for success/error feedback
- [ ] Verify all INSERT operations with parameterized queries (no raw string concat)
- [ ] Manual walkthrough: User registers → browses routes → books → views booking
- [ ] Manual walkthrough: Admin logs in → views bookings → views payments
- [ ] Update `newREADME.md` with frontend run instructions
- [ ] Git commit: `feat(frontend): complete prototype with user and admin portals`

---

## Phase F — Version Control Hygiene

- [ ] Add `frontend/__pycache__/` to `.gitignore`
- [ ] Commit `plan.md` + `todo.md` first: `docs(frontend): add plan and todo`
- [ ] Commit Phase A–B: `feat(frontend): foundation — db, app skeleton, base styles`
- [ ] Commit Phase C: `feat(frontend): user portal complete`
- [ ] Commit Phase D: `feat(frontend): admin portal complete`
- [ ] Commit Phase E: `feat(frontend): session guards, flash messages, verification`
