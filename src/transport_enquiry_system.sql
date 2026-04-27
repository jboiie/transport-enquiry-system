CREATE DATABASE transport_enquiry_system;
USE transport_enquiry_system;
CREATE TABLE USER (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE
);
CREATE TABLE USER_PHONE (
    user_id INT,
    phone VARCHAR(15),
    PRIMARY KEY (user_id, phone),
    FOREIGN KEY (user_id) REFERENCES USER(user_id)
        ON DELETE CASCADE
);
CREATE TABLE ENQUIRY (
    user_id INT,
    enquiry_number INT,
    enquiry_date DATE,
    enquiry_text TEXT,
    status VARCHAR(50),
    PRIMARY KEY (user_id, enquiry_number),
    FOREIGN KEY (user_id) REFERENCES USER(user_id)
        ON DELETE CASCADE
);
CREATE TABLE TRANSPORT (
    transport_id INT PRIMARY KEY AUTO_INCREMENT,
    transport_type VARCHAR(50),
    capacity INT
);
CREATE TABLE ROUTE (
    route_id INT PRIMARY KEY AUTO_INCREMENT,
    source VARCHAR(100),
    destination VARCHAR(100),
    distance DECIMAL(8,2)
);
CREATE TABLE STATION (
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    station_name VARCHAR(100),
    city VARCHAR(100)
);
CREATE TABLE ROUTE_STATION (
    route_id INT,
    station_id INT,
    PRIMARY KEY (route_id, station_id),
    FOREIGN KEY (route_id) REFERENCES ROUTE(route_id)
        ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES STATION(station_id)
        ON DELETE CASCADE
);
CREATE TABLE SCHEDULE (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    departure_time TIME,
    arrival_time TIME,
    date DATE,
    transport_id INT,
    route_id INT,
    FOREIGN KEY (transport_id) REFERENCES TRANSPORT(transport_id),
    FOREIGN KEY (route_id) REFERENCES ROUTE(route_id)
);
CREATE TABLE BOOKING (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_date DATE,
    seat_number VARCHAR(10),
    user_id INT,
    schedule_id INT,
    FOREIGN KEY (user_id) REFERENCES USER(user_id),
    FOREIGN KEY (schedule_id) REFERENCES SCHEDULE(schedule_id)
);
CREATE TABLE PAYMENT (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    payment_mode VARCHAR(50),
    payment_status VARCHAR(50),
    booking_id INT UNIQUE,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id)
        ON DELETE CASCADE
);
SELECT 
    route_id,
    source,
    destination,
    distance,
    (distance / 60) AS travel_time_hours
FROM ROUTE;
SHOW TABLES;
DESCRIBE USER;
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
SELECT 
    r.source,
    r.destination,
    s.departure_time,
    s.arrival_time,
    t.transport_type
FROM SCHEDULE s
JOIN ROUTE r ON s.route_id = r.route_id
JOIN TRANSPORT t ON s.transport_id = t.transport_id
WHERE r.source = 'Chennai'
AND r.destination = 'Bangalore';
SELECT 
    u.first_name,
    b.booking_id,
    b.seat_number,
    s.date
FROM BOOKING b
JOIN USER u ON b.user_id = u.user_id
JOIN SCHEDULE s ON b.schedule_id = s.schedule_id
WHERE u.first_name = 'Rahul';
INSERT INTO ENQUIRY (user_id, enquiry_number, enquiry_date, status)
VALUES (1, 1, '2026-02-09', 'Resolved');
SELECT * FROM ENQUIRY;

