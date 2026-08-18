CREATE DATABASE ola_analytics;
USE ola_analytics;
SELECT DATABASE();
USE ola_analytics;

SHOW TABLES;
SELECT COUNT(*) AS total_rows
FROM bookings_cleaned;
DESCRIBE bookings_cleaned;
SELECT * 
FROM bookings_cleaned
LIMIT 5;

SELECT
    COUNT(*) AS total_bookings,
    SUM(Is_Successful) AS successful_bookings,
    COUNT(*) - SUM(Is_Successful) AS unsuccessful_bookings,
    ROUND(SUM(Is_Successful) * 100.0 / COUNT(*), 2) AS success_rate,
    ROUND((COUNT(*) - SUM(Is_Successful)) * 100.0 / COUNT(*), 2) AS unsuccessful_rate
FROM bookings_cleaned;

SELECT
    Booking_Status,
    COUNT(*) AS total_bookings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings_cleaned), 2) AS percentage
FROM bookings_cleaned
GROUP BY Booking_Status
ORDER BY total_bookings DESC;

SELECT
    Booking_Hour,
    COUNT(*) AS total_bookings
FROM bookings_cleaned
GROUP BY Booking_Hour
ORDER BY Booking_Hour;

SELECT
    Booking_Day_Type,
    COUNT(*) AS total_bookings,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM bookings_cleaned),
        2
    ) AS percentage
FROM bookings_cleaned
GROUP BY Booking_Day_Type
ORDER BY total_bookings DESC;

SELECT
    Vehicle_Type,
    COUNT(*) AS total_bookings
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY total_bookings DESC;

SELECT
    Vehicle_Type,
    SUM(Booking_Value) AS total_revenue
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY total_revenue DESC;

SELECT
    Vehicle_Type,
    ROUND(AVG(Booking_Value), 2) AS average_booking_value
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY average_booking_value DESC;

SELECT
    Vehicle_Type,
    ROUND(AVG(Is_Successful) * 100, 2) AS success_rate
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY success_rate DESC;

SELECT
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS average_ride_distance
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY average_ride_distance DESC;

SELECT
    Cancellation_Type,
    COUNT(*) AS total_bookings,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM bookings_cleaned),
        2
    ) AS percentage
FROM bookings_cleaned
GROUP BY Cancellation_Type
ORDER BY total_bookings DESC;

SELECT
    Canceled_Rides_by_Customer AS cancellation_reason,
    COUNT(*) AS total_cancellations
FROM bookings_cleaned
WHERE Canceled_Rides_by_Customer IS NOT NULL
  AND Canceled_Rides_by_Customer <> ''
GROUP BY Canceled_Rides_by_Customer
ORDER BY total_cancellations DESC;

SELECT
    Canceled_Rides_by_Driver AS cancellation_reason,
    COUNT(*) AS total_cancellations
FROM bookings_cleaned
WHERE Canceled_Rides_by_Driver IS NOT NULL
  AND Canceled_Rides_by_Driver <> ''
GROUP BY Canceled_Rides_by_Driver
ORDER BY total_cancellations DESC;

SELECT
    Incomplete_Rides_Reason AS reason,
    COUNT(*) AS total_incomplete_rides
FROM bookings_cleaned
WHERE Incomplete_Rides_Reason IS NOT NULL
  AND Incomplete_Rides_Reason <> ''
GROUP BY Incomplete_Rides_Reason
ORDER BY total_incomplete_rides DESC;

SELECT
    Payment_Method,
    COUNT(*) AS total_bookings,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM bookings_cleaned
         WHERE Payment_Method IS NOT NULL
         AND Payment_Method <> ''),
        2
    ) AS percentage
FROM bookings_cleaned
WHERE Payment_Method IS NOT NULL
  AND Payment_Method <> ''
GROUP BY Payment_Method
ORDER BY total_bookings DESC;

SELECT
    Payment_Method,
    SUM(Booking_Value) AS total_revenue
FROM bookings_cleaned
WHERE Payment_Method IS NOT NULL
  AND Payment_Method <> ''
GROUP BY Payment_Method
ORDER BY total_revenue DESC;

SELECT
    Pickup_Location,
    COUNT(*) AS total_bookings
FROM bookings_cleaned
GROUP BY Pickup_Location
ORDER BY total_bookings DESC
LIMIT 10;

SELECT
    Drop_Location,
    COUNT(*) AS total_bookings
FROM bookings_cleaned
GROUP BY Drop_Location
ORDER BY total_bookings DESC
LIMIT 10;

SELECT
    Payment_Method,
    ROUND(AVG(Booking_Value), 2) AS average_booking_value
FROM bookings_cleaned
WHERE Payment_Method IS NOT NULL
  AND Payment_Method <> ''
GROUP BY Payment_Method
ORDER BY average_booking_value DESC;

SELECT
    Vehicle_Type,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END) AS unsuccessful_bookings,
    ROUND(
        SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS unsuccessful_rate
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY unsuccessful_rate DESC;

SELECT
    Booking_Hour,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END) AS unsuccessful_bookings,
    ROUND(
        SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS unsuccessful_rate
FROM bookings_cleaned
GROUP BY Booking_Hour
ORDER BY unsuccessful_rate DESC;

SELECT
    Booking_Day_Type,
    COUNT(*) AS total_bookings,
    SUM(Is_Successful) AS successful_bookings,
    ROUND(AVG(Is_Successful) * 100, 2) AS success_rate,
    ROUND(
        (1 - AVG(Is_Successful)) * 100,
        2
    ) AS unsuccessful_rate
FROM bookings_cleaned
GROUP BY Booking_Day_Type;

SELECT
    Pickup_Location,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END) AS unsuccessful_bookings,
    ROUND(
        SUM(CASE WHEN Is_Successful = 0 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS unsuccessful_rate
FROM bookings_cleaned
GROUP BY Pickup_Location
HAVING COUNT(*) >= 100
ORDER BY unsuccessful_rate DESC
LIMIT 10;

SELECT
    CASE
        WHEN Ride_Distance = 0 THEN '0 km'
        WHEN Ride_Distance <= 10 THEN '1-10 km'
        WHEN Ride_Distance <= 20 THEN '11-20 km'
        WHEN Ride_Distance <= 30 THEN '21-30 km'
        ELSE '31+ km'
    END AS distance_range,

    COUNT(*) AS total_bookings,

    ROUND(AVG(Booking_Value), 2) AS average_booking_value,

    ROUND(AVG(Ride_Distance), 2) AS average_distance

FROM bookings_cleaned

GROUP BY distance_range

ORDER BY average_distance;

WITH vehicle_performance AS (
    SELECT
        Vehicle_Type,
        COUNT(*) AS total_bookings,
        ROUND(AVG(Is_Successful) * 100, 2) AS success_rate,
        ROUND(AVG(Booking_Value), 2) AS avg_booking_value
    FROM bookings_cleaned
    GROUP BY Vehicle_Type
)

SELECT
    Vehicle_Type,
    total_bookings,
    success_rate,
    avg_booking_value
FROM vehicle_performance
ORDER BY success_rate DESC;

SELECT
    Vehicle_Type,
    ROUND(AVG(Is_Successful) * 100, 2) AS success_rate,
    RANK() OVER (
        ORDER BY AVG(Is_Successful) DESC
    ) AS success_rank
FROM bookings_cleaned
GROUP BY Vehicle_Type
ORDER BY success_rank;

WITH location_bookings AS (
    SELECT
        Pickup_Location,
        COUNT(*) AS total_bookings
    FROM bookings_cleaned
    GROUP BY Pickup_Location
)

SELECT
    Pickup_Location,
    total_bookings,
    RANK() OVER (
        ORDER BY total_bookings DESC
    ) AS booking_rank
FROM location_bookings
ORDER BY booking_rank
LIMIT 10;

SELECT
    Booking_ID,
    Vehicle_Type,
    Pickup_Location,
    Drop_Location,
    Ride_Distance,
    Booking_Value,
    Driver_Ratings
FROM bookings_cleaned
WHERE Is_Successful = 1
  AND Booking_Value > (
      SELECT AVG(Booking_Value)
      FROM bookings_cleaned
  )
ORDER BY Booking_Value DESC
LIMIT 20;

SELECT
    COUNT(*) AS total_bookings,

    SUM(Is_Successful) AS successful_bookings,

    COUNT(*) - SUM(Is_Successful) AS unsuccessful_bookings,

    ROUND(AVG(Is_Successful) * 100, 2) AS success_rate,

    SUM(Booking_Value) AS total_revenue,

    ROUND(AVG(Booking_Value), 2) AS avg_booking_value,

    ROUND(AVG(Ride_Distance), 2) AS avg_ride_distance,

    ROUND(AVG(Driver_Ratings), 2) AS avg_driver_rating,

    ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating

FROM bookings_cleaned;