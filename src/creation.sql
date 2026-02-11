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