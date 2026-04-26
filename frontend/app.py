"""
app.py — Flask application (all routes)
========================================
Run:  python app.py
Then open: http://localhost:5000
"""
import math
from datetime import date
from functools import wraps

import mysql.connector
from flask import (Flask, flash, redirect, render_template,
                   request, session, url_for)

from db import get_db

app = Flask(__name__)
app.secret_key = 'tes2024-secret-transport-key'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


def generate_seats(capacity):
    """Generate seat labels A1..ZN up to capacity (10 per row)."""
    seats, cols = [], 10
    rows = math.ceil(capacity / cols)
    for r in range(min(rows, 26)):
        for c in range(1, cols + 1):
            if len(seats) >= capacity:
                return seats
            seats.append(f"{chr(65 + r)}{c}")
    return seats


def calc_fare(distance, transport_type):
    rate = 2.0 if transport_type == 'Bus' else 1.5
    return round(float(distance) * rate, 2)


# ──────────────────────────────────────────────────────────────
# Landing
# ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ──────────────────────────────────────────────────────────────
# User — Auth
# ──────────────────────────────────────────────────────────────

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        action = request.form.get('action', 'login')
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        try:
            if action == 'login':
                email = request.form['email'].strip()
                cur.execute("SELECT * FROM USER WHERE email = %s", (email,))
                user = cur.fetchone()
                if user:
                    session['user_id'] = user['user_id']
                    session['user_name'] = user['first_name']
                    flash(f"Welcome back, {user['first_name']}!", 'success')
                    return redirect(url_for('user_dashboard'))
                flash('Email not found. Register below.', 'error')
                return render_template('user/login.html', show_register=True, prefill_email=email)

            elif action == 'register':
                fn   = request.form['first_name'].strip()
                ln   = request.form['last_name'].strip()
                email = request.form['email'].strip()
                phone = request.form['phone'].strip()
                cur.execute(
                    "INSERT INTO USER (first_name, last_name, email) VALUES (%s,%s,%s)",
                    (fn, ln, email))
                uid = cur.lastrowid
                cur.execute(
                    "INSERT INTO USER_PHONE (user_id, phone) VALUES (%s,%s)",
                    (uid, phone))
                conn.commit()
                session['user_id'] = uid
                session['user_name'] = fn
                flash(f"Account created! Welcome, {fn}!", 'success')
                return redirect(url_for('user_dashboard'))
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Error: {e.msg}", 'error')
        finally:
            cur.close(); conn.close()
    return render_template('user/login.html')


@app.route('/user/logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


# ──────────────────────────────────────────────────────────────
# User — Dashboard
# ──────────────────────────────────────────────────────────────

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    uid = session['user_id']
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as c FROM BOOKING WHERE user_id=%s", (uid,))
    booking_count = cur.fetchone()['c']
    cur.execute("""SELECT COUNT(*) as c FROM PAYMENT p
                   JOIN BOOKING b ON p.booking_id=b.booking_id
                   WHERE b.user_id=%s AND p.payment_status='Pending'""", (uid,))
    pending_count = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) as c FROM ENQUIRY WHERE user_id=%s", (uid,))
    enquiry_count = cur.fetchone()['c']
    cur.execute("""
        SELECT b.booking_id, r.source, r.destination, s.date, b.seat_number,
               p.payment_status
        FROM BOOKING b
        JOIN SCHEDULE s ON b.schedule_id=s.schedule_id
        JOIN ROUTE r ON s.route_id=r.route_id
        LEFT JOIN PAYMENT p ON p.booking_id=b.booking_id
        WHERE b.user_id=%s ORDER BY b.booking_id DESC LIMIT 3""", (uid,))
    recent = cur.fetchall()
    cur.close(); conn.close()
    return render_template('user/dashboard.html',
                           booking_count=booking_count,
                           pending_count=pending_count,
                           enquiry_count=enquiry_count,
                           recent=recent)


# ──────────────────────────────────────────────────────────────
# User — Browse Routes / Schedules
# ──────────────────────────────────────────────────────────────

@app.route('/user/routes')
@login_required
def user_routes():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    src = request.args.get('source', '').strip()
    dst = request.args.get('destination', '').strip()
    sql = """
        SELECT s.schedule_id, r.source, r.destination, r.distance,
               s.date, s.departure_time, s.arrival_time,
               t.transport_type, t.capacity,
               (SELECT COUNT(*) FROM BOOKING WHERE schedule_id=s.schedule_id) AS booked
        FROM SCHEDULE s
        JOIN ROUTE r ON s.route_id=r.route_id
        JOIN TRANSPORT t ON s.transport_id=t.transport_id
        WHERE 1=1"""
    params = []
    if src: sql += " AND r.source LIKE %s";      params.append(f'%{src}%')
    if dst: sql += " AND r.destination LIKE %s"; params.append(f'%{dst}%')
    sql += " ORDER BY s.date, s.departure_time"
    cur.execute(sql, params)
    schedules = cur.fetchall()
    cur.execute("SELECT DISTINCT source FROM ROUTE ORDER BY source")
    sources = [r['source'] for r in cur.fetchall()]
    cur.execute("SELECT DISTINCT destination FROM ROUTE ORDER BY destination")
    destinations = [r['destination'] for r in cur.fetchall()]
    cur.close(); conn.close()
    return render_template('user/routes.html', schedules=schedules,
                           sources=sources, destinations=destinations,
                           src=src, dst=dst)


# ──────────────────────────────────────────────────────────────
# User — Book
# ──────────────────────────────────────────────────────────────

@app.route('/user/book/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def user_book(schedule_id):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.schedule_id, r.source, r.destination, r.distance,
               s.date, s.departure_time, s.arrival_time,
               t.transport_type, t.capacity
        FROM SCHEDULE s
        JOIN ROUTE r ON s.route_id=r.route_id
        JOIN TRANSPORT t ON s.transport_id=t.transport_id
        WHERE s.schedule_id=%s""", (schedule_id,))
    schedule = cur.fetchone()
    if not schedule:
        flash('Schedule not found.', 'error')
        return redirect(url_for('user_routes'))

    cur.execute("SELECT seat_number FROM BOOKING WHERE schedule_id=%s", (schedule_id,))
    booked = {r['seat_number'] for r in cur.fetchall()}
    all_seats = generate_seats(schedule['capacity'])
    fare = calc_fare(schedule['distance'], schedule['transport_type'])

    if request.method == 'POST':
        seat = request.form.get('seat_number', '').strip()
        mode = request.form.get('payment_mode', '').strip()
        if not seat or seat not in all_seats or seat in booked:
            flash('Invalid or already-booked seat. Pick another.', 'error')
        else:
            try:
                cur.execute(
                    "INSERT INTO BOOKING (booking_date,seat_number,user_id,schedule_id) VALUES (%s,%s,%s,%s)",
                    (date.today().isoformat(), seat, session['user_id'], schedule_id))
                bid = cur.lastrowid
                cur.execute(
                    "INSERT INTO PAYMENT (amount,payment_mode,payment_status,booking_id) VALUES (%s,%s,'Pending',%s)",
                    (fare, mode, bid))
                conn.commit()
                flash(f"Booking confirmed! Seat {seat} | ₹{fare}", 'success')
                cur.close(); conn.close()
                return redirect(url_for('user_bookings'))
            except mysql.connector.Error as e:
                conn.rollback()
                flash(f"Booking failed: {e.msg}", 'error')

    cur.close(); conn.close()
    return render_template('user/book.html', schedule=schedule,
                           booked=list(booked), all_seats=all_seats, fare=fare)


# ──────────────────────────────────────────────────────────────
# User — My Bookings + Cancel
# ──────────────────────────────────────────────────────────────

@app.route('/user/bookings')
@login_required
def user_bookings():
    uid = session['user_id']
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.booking_id, r.source, r.destination, s.date, s.departure_time,
               b.seat_number, b.booking_date,
               p.amount, p.payment_mode, p.payment_status
        FROM BOOKING b
        JOIN SCHEDULE s ON b.schedule_id=s.schedule_id
        JOIN ROUTE r ON s.route_id=r.route_id
        LEFT JOIN PAYMENT p ON p.booking_id=b.booking_id
        WHERE b.user_id=%s ORDER BY b.booking_id DESC""", (uid,))
    bookings = cur.fetchall()
    cur.close(); conn.close()
    return render_template('user/bookings.html', bookings=bookings)


@app.route('/user/cancel/<int:booking_id>', methods=['POST'])
@login_required
def user_cancel(booking_id):
    uid = session['user_id']
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT booking_id FROM BOOKING WHERE booking_id=%s AND user_id=%s",
                (booking_id, uid))
    if not cur.fetchone():
        flash('Booking not found or unauthorized.', 'error')
    else:
        try:
            cur.execute("DELETE FROM BOOKING WHERE booking_id=%s", (booking_id,))
            conn.commit()
            flash('Booking cancelled.', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Error: {e.msg}", 'error')
    cur.close(); conn.close()
    return redirect(url_for('user_bookings'))


# ──────────────────────────────────────────────────────────────
# User — Enquiry
# ──────────────────────────────────────────────────────────────

@app.route('/user/enquiry', methods=['GET', 'POST'])
@login_required
def user_enquiry():
    uid = session['user_id']
    conn = get_db(); cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cur.execute(
            "SELECT COALESCE(MAX(enquiry_number),0)+1 AS n FROM ENQUIRY WHERE user_id=%s", (uid,))
        nxt = cur.fetchone()['n']
        try:
            cur.execute(
                "INSERT INTO ENQUIRY (user_id,enquiry_number,enquiry_date,status) VALUES (%s,%s,%s,'Open')",
                (uid, nxt, date.today().isoformat()))
            conn.commit()
            flash('Enquiry submitted!', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Error: {e.msg}", 'error')
    cur.execute("SELECT * FROM ENQUIRY WHERE user_id=%s ORDER BY enquiry_number DESC", (uid,))
    enquiries = cur.fetchall()
    cur.close(); conn.close()
    return render_template('user/enquiry.html', enquiries=enquiries)


# ──────────────────────────────────────────────────────────────
# Admin — Auth
# ──────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if (request.form.get('username') == ADMIN_USERNAME and
                request.form.get('password') == ADMIN_PASSWORD):
            session['is_admin'] = True
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


# ──────────────────────────────────────────────────────────────
# Admin — Dashboard
# ──────────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    def count(q, p=()):
        cur.execute(q, p); return cur.fetchone()

    stats = {
        'users':     count("SELECT COUNT(*) c FROM USER")['c'],
        'bookings':  count("SELECT COUNT(*) c FROM BOOKING")['c'],
        'revenue':   count("SELECT COALESCE(SUM(amount),0) c FROM PAYMENT WHERE payment_status='Completed'")['c'],
        'pending':   count("SELECT COUNT(*) c FROM PAYMENT WHERE payment_status='Pending'")['c'],
        'routes':    count("SELECT COUNT(*) c FROM ROUTE")['c'],
        'schedules': count("SELECT COUNT(*) c FROM SCHEDULE")['c'],
    }
    cur.execute("""
        SELECT b.booking_id, u.first_name, u.last_name,
               r.source, r.destination, b.seat_number, s.date, p.payment_status
        FROM BOOKING b
        JOIN USER u ON b.user_id=u.user_id
        JOIN SCHEDULE s ON b.schedule_id=s.schedule_id
        JOIN ROUTE r ON s.route_id=r.route_id
        LEFT JOIN PAYMENT p ON p.booking_id=b.booking_id
        ORDER BY b.booking_id DESC LIMIT 6""")
    recent = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/dashboard.html', stats=stats, recent=recent)


# ──────────────────────────────────────────────────────────────
# Admin — All Bookings
# ──────────────────────────────────────────────────────────────

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.booking_id, u.first_name, u.last_name, u.email,
               r.source, r.destination, s.date, s.departure_time,
               b.seat_number, b.booking_date,
               p.amount, p.payment_mode, p.payment_status
        FROM BOOKING b
        JOIN USER u ON b.user_id=u.user_id
        JOIN SCHEDULE s ON b.schedule_id=s.schedule_id
        JOIN ROUTE r ON s.route_id=r.route_id
        LEFT JOIN PAYMENT p ON p.booking_id=b.booking_id
        ORDER BY b.booking_id DESC""")
    bookings = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/bookings.html', bookings=bookings)


# ──────────────────────────────────────────────────────────────
# Admin — Routes CRUD
# ──────────────────────────────────────────────────────────────

@app.route('/admin/routes')
@admin_required
def admin_routes():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM ROUTE ORDER BY route_id")
    routes = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/routes.html', routes=routes)


@app.route('/admin/routes/add', methods=['POST'])
@admin_required
def admin_add_route():
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ROUTE (source,destination,distance) VALUES (%s,%s,%s)",
                    (request.form['source'].strip(),
                     request.form['destination'].strip(),
                     float(request.form['distance'])))
        conn.commit()
        flash('Route added.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_routes'))


@app.route('/admin/routes/delete/<int:route_id>', methods=['POST'])
@admin_required
def admin_delete_route(route_id):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM ROUTE WHERE route_id=%s", (route_id,))
        conn.commit(); flash('Route deleted.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_routes'))


# ──────────────────────────────────────────────────────────────
# Admin — Transports CRUD
# ──────────────────────────────────────────────────────────────

@app.route('/admin/transports')
@admin_required
def admin_transports():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM TRANSPORT ORDER BY transport_id")
    transports = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/transports.html', transports=transports)


@app.route('/admin/transports/add', methods=['POST'])
@admin_required
def admin_add_transport():
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO TRANSPORT (transport_type,capacity) VALUES (%s,%s)",
                    (request.form['transport_type'].strip(), int(request.form['capacity'])))
        conn.commit(); flash('Transport added.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_transports'))


@app.route('/admin/transports/delete/<int:tid>', methods=['POST'])
@admin_required
def admin_delete_transport(tid):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM TRANSPORT WHERE transport_id=%s", (tid,))
        conn.commit(); flash('Transport deleted.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_transports'))


# ──────────────────────────────────────────────────────────────
# Admin — Schedules CRUD
# ──────────────────────────────────────────────────────────────

@app.route('/admin/schedules')
@admin_required
def admin_schedules():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.schedule_id, r.source, r.destination, s.date,
               s.departure_time, s.arrival_time, t.transport_type, t.capacity
        FROM SCHEDULE s
        JOIN ROUTE r ON s.route_id=r.route_id
        JOIN TRANSPORT t ON s.transport_id=t.transport_id
        ORDER BY s.date DESC, s.departure_time""")
    schedules = cur.fetchall()
    cur.execute("SELECT * FROM ROUTE ORDER BY source")
    routes = cur.fetchall()
    cur.execute("SELECT * FROM TRANSPORT ORDER BY transport_type")
    transports = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/schedules.html',
                           schedules=schedules, routes=routes, transports=transports)


@app.route('/admin/schedules/add', methods=['POST'])
@admin_required
def admin_add_schedule():
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO SCHEDULE (departure_time,arrival_time,date,transport_id,route_id) VALUES (%s,%s,%s,%s,%s)",
            (request.form['departure_time'], request.form['arrival_time'],
             request.form['date'], int(request.form['transport_id']),
             int(request.form['route_id'])))
        conn.commit(); flash('Schedule added.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_schedules'))


@app.route('/admin/schedules/delete/<int:sid>', methods=['POST'])
@admin_required
def admin_delete_schedule(sid):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM SCHEDULE WHERE schedule_id=%s", (sid,))
        conn.commit(); flash('Schedule deleted.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_schedules'))


# ──────────────────────────────────────────────────────────────
# Admin — Payments
# ──────────────────────────────────────────────────────────────

@app.route('/admin/payments')
@admin_required
def admin_payments():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.payment_id, p.amount, p.payment_mode, p.payment_status,
               b.booking_id, b.seat_number, u.first_name, u.last_name,
               r.source, r.destination, s.date
        FROM PAYMENT p
        JOIN BOOKING b ON p.booking_id=b.booking_id
        JOIN USER u ON b.user_id=u.user_id
        JOIN SCHEDULE s ON b.schedule_id=s.schedule_id
        JOIN ROUTE r ON s.route_id=r.route_id
        ORDER BY p.payment_id DESC""")
    payments = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/payments.html', payments=payments)


@app.route('/admin/payments/update/<int:payment_id>', methods=['POST'])
@admin_required
def admin_update_payment(payment_id):
    new_status = request.form.get('payment_status', 'Pending')
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("UPDATE PAYMENT SET payment_status=%s WHERE payment_id=%s",
                    (new_status, payment_id))
        conn.commit(); flash('Payment status updated.', 'success')
    except mysql.connector.Error as e:
        conn.rollback(); flash(f"Error: {e.msg}", 'error')
    finally:
        cur.close(); conn.close()
    return redirect(url_for('admin_payments'))


# ──────────────────────────────────────────────────────────────
# Admin — Users (view only)
# ──────────────────────────────────────────────────────────────

@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT u.user_id, u.first_name, u.last_name, u.email,
               GROUP_CONCAT(up.phone SEPARATOR ', ') AS phones,
               COUNT(DISTINCT b.booking_id) AS booking_count
        FROM USER u
        LEFT JOIN USER_PHONE up ON u.user_id=up.user_id
        LEFT JOIN BOOKING b ON u.user_id=b.user_id
        GROUP BY u.user_id ORDER BY u.user_id DESC""")
    users = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin/users.html', users=users)


# ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
