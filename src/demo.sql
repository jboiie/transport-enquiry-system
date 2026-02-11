USE transport_enquiry_system;
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

SELECT * FROM ENQUIRY;