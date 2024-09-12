-- Start the transaction
START TRANSACTION;

-- Create a booking document
UPSERT INTO bookings
VALUES("bf7ad6fa-bdb9-4099-a840-196e47179f03", {
  "date": "07/24/2021",
  "flight": "WN533",
  "flighttime": 7713,
  "price": 964.13,
  "route": "63986"
});

-- Set a savepoint
SAVEPOINT s1;

-- Update the booking document to include a user
UPDATE bookings AS b
SET b.`user` = "0"
WHERE META(b).id = "bf7ad6fa-bdb9-4099-a840-196e47179f03";

-- Check the content of the booking and user
SELECT b.*, u.name
FROM bookings b
JOIN users u
ON b.`user` = META(u).id
WHERE META(b).id = "bf7ad6fa-bdb9-4099-a840-196e47179f03";

-- Set a second savepoint
SAVEPOINT s2;

-- Update the booking documents to change the user
UPDATE bookings AS b
SET b.`user` = "1"
WHERE META(b).id = "bf7ad6fa-bdb9-4099-a840-196e47179f03";

-- Check the content of the booking and user
SELECT b.*, u.name
FROM bookings b
JOIN users u
ON b.`user` = META(u).id
WHERE META(b).id = "bf7ad6fa-bdb9-4099-a840-196e47179f03";

-- Roll back the transaction to the second savepoint
ROLLBACK TRAN TO SAVEPOINT s2;

-- Check the content of the booking and user again
SELECT b.*, u.name
FROM bookings b
JOIN users u
ON b.`user` = META(u).id
WHERE META(b).id = "bf7ad6fa-bdb9-4099-a840-196e47179f03";

-- Commit the transaction
COMMIT TRANSACTION;
