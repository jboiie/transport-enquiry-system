USE transport_enquiry_system;


INSERT INTO USER (first_name, last_name, email) VALUES
('Rahul', 'Sharma', 'rahul.sharma@email.com'),
('Priya', 'Menon', 'priya.menon@email.com'),
('Arjun', 'Reddy', 'arjun.reddy@email.com');

INSERT INTO USER_PHONE (user_id, phone) VALUES
(1, '9876543210'),
(1, '9123456780'),
(2, '9988776655'),
(3, '9090909090');

INSERT INTO TRANSPORT (transport_type, capacity) VALUES
('Bus', 50),
('Train', 500);

INSERT INTO ROUTE (source, destination, distance) VALUES
('Chennai', 'Bangalore', 350.00),
('Chennai', 'Hyderabad', 630.00),
('Bangalore', 'Mysore', 150.00);

INSERT INTO STATION (station_name, city) VALUES
('Chennai Central', 'Chennai'),
('Bangalore City', 'Bangalore'),
('Hyderabad Deccan', 'Hyderabad'),
('Mysore Junction', 'Mysore');

INSERT INTO ROUTE_STATION (route_id, station_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 2),
(3, 4);

INSERT INTO SCHEDULE (departure_time, arrival_time, date, transport_id, route_id) VALUES
('08:00:00', '14:00:00', '2026-02-15', 1, 1),
('09:00:00', '20:00:00', '2026-02-16', 2, 2),
('07:30:00', '10:00:00', '2026-02-17', 1, 3);

INSERT INTO BOOKING (booking_date, seat_number, user_id, schedule_id) VALUES
('2026-02-10', 'A1', 1, 1),
('2026-02-11', 'B2', 2, 2),
('2026-02-12', 'C3', 3, 3);

INSERT INTO PAYMENT (amount, payment_mode, payment_status, booking_id) VALUES
(750.00, 'UPI', 'Completed', 1),
(1200.00, 'Credit Card', 'Completed', 2),
(400.00, 'Cash', 'Pending', 3);

INSERT INTO ENQUIRY (user_id, enquiry_number, enquiry_date, status)
VALUES (1, 1, '2026-02-09', 'Resolved');