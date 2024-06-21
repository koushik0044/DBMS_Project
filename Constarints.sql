USE Project;

-- USER TABLE CONSTARINTS
-- Add a CHECK constraint for phone numbers to match a specific pattern (basic example)
ALTER TABLE Users
ADD CONSTRAINT CHK_Users_PhoneNumber CHECK (CHAR_LENGTH(PhoneNumber) = 10 AND PhoneNumber NOT LIKE '%[^0-9]%');

-- Add a UNIQUE constraint for email if it wasn't set during table creation
ALTER TABLE Users
ADD CONSTRAINT UQ_Users_Email UNIQUE (Email);

ALTER TABLE Users
ADD CONSTRAINT CHK_Users_Email_Format CHECK (Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$');

-- Theaters constarints
-- Add a UNIQUE constraint for theater names
ALTER TABLE Theaters
ADD CONSTRAINT UQ_Theater_Name UNIQUE (Name);

-- Add a CHECK constraint to ensure TotalSeats is a positive integer
ALTER TABLE Theaters
ADD CONSTRAINT CHK_Theater_TotalSeats CHECK (TotalSeats > 0);

-- Add a CHECK constraint to ensure NumberOfScreens is a positive integer
ALTER TABLE Theaters
ADD CONSTRAINT CHK_Theater_NumberOfScreens CHECK (NumberOfScreens > 0);

-- Add a CHECK constraint for the PostalCode format (simple US format example)
ALTER TABLE Theaters
ADD CONSTRAINT CHK_Theater_PostalCode CHECK (CHAR_LENGTH(PostalCode) = 5 AND PostalCode NOT LIKE '%[^0-9]%');

-- Add a CHECK constraint for phone numbers to match a specific pattern (basic example)
ALTER TABLE Theaters
ADD CONSTRAINT CHK_Theaters_PhoneNumber CHECK (CHAR_LENGTH(PhoneNumber) = 10 AND PhoneNumber NOT LIKE '%[^0-9]%');

-- Movie Constraints
-- Add a UNIQUE constraint for movie titles
ALTER TABLE Movies
ADD CONSTRAINT UQ_Movie_Title UNIQUE (Title);

-- Add a CHECK constraint to ensure Duration is a positive integer and perhaps not exceeding, say, 500 minutes
ALTER TABLE Movies
ADD CONSTRAINT CHK_Movie_Duration CHECK (Duration > 0 AND Duration <= 500);

-- Screens Constraints
-- Add a CHECK constraint to ensure SeatCapacity is a positive integer
ALTER TABLE Screens
ADD CONSTRAINT CHK_Screens_SeatCapacity CHECK (SeatCapacity > 0);

-- Add a UNIQUE constraint to ensure ScreenName is unique within the same theater
-- This requires a compound unique constraint on both ScreenName and TheaterID
ALTER TABLE Screens
ADD CONSTRAINT UQ_ScreenName_TheaterID UNIQUE (ScreenName, TheaterID);


-- ShowTimes Constraints
-- Add a CHECK constraint to ensure TicketPrice is a positive number
ALTER TABLE Showtimes
ADD CONSTRAINT CHK_Showtimes_TicketPrice CHECK (TicketPrice >= 0);

-- Add a CHECK constraint to ensure StartTime is earlier than EndTime
ALTER TABLE Showtimes
ADD CONSTRAINT CHK_Showtimes_StartBeforeEnd CHECK (StartTime < EndTime);


-- Tickets Constraints
-- Add a CHECK constraint to ensure TotalAmount is a positive number
ALTER TABLE Tickets
ADD CONSTRAINT CHK_Tickets_TotalAmount CHECK (TotalAmount >= 0);

-- If SeatNumber must follow a specific format, add a CHECK constraint for it
-- Example: Seats are like 'A10', 'B15', etc., where the first character is a letter and the following two are digits
ALTER TABLE Tickets
ADD CONSTRAINT CHK_Tickets_SeatNumber CHECK (SeatNumber REGEXP '^[A-Z][0-9]{2}$');

-- Ensure that the same seat is not double-booked for the same showtime
-- This requires creating a unique index on the combination of ShowtimeID and SeatNumber
ALTER TABLE Tickets
ADD CONSTRAINT UQ_Tickets_Showtime_Seat UNIQUE (ShowtimeID, SeatNumber);


-- Payments Constraints
-- Add a CHECK constraint to ensure Amount is a positive number
ALTER TABLE Payments
ADD CONSTRAINT CHK_Payments_Amount CHECK (Amount >= 0);

-- Add a CHECK constraint to ensure PaymentMethod is within a list of accepted methods
ALTER TABLE Payments
ADD CONSTRAINT CHK_Payments_Method CHECK (PaymentMethod IN ('Credit Card', 'PayPal', 'Bank Transfer', 'Cash'));

-- Add a CHECK constraint to ensure PaymentStatus is within a list of accepted statuses
ALTER TABLE Payments
ADD CONSTRAINT CHK_Payments_Status CHECK (PaymentStatus IN ('Completed', 'Pending', 'Failed', 'Refunded'));

-- Add a UNIQUE constraint to ensure TransactionID is unique if not null
ALTER TABLE Payments
ADD CONSTRAINT UQ_Payments_TransactionID UNIQUE (TransactionID);

-- Promotions Constraints
-- Add a UNIQUE constraint for the promo code
ALTER TABLE Promotions
ADD CONSTRAINT UQ_Promotions_Code UNIQUE (Code);

-- Add a CHECK constraint to ensure the discount percentage is between 0 and 100
ALTER TABLE Promotions
ADD CONSTRAINT CHK_Promotions_Discount CHECK (DiscountPercentage BETWEEN 0 AND 100);

-- Add a CHECK constraint to ensure the ValidFrom date comes before the ValidTill date
ALTER TABLE Promotions
ADD CONSTRAINT CHK_Promotions_Validity CHECK (ValidFrom < ValidTill);


-- RatingsReviews constraints
-- Add a CHECK constraint to ensure Rating is between 1 and 10
ALTER TABLE RatingsReviews
ADD CONSTRAINT CHK_RatingsReviews_Rating CHECK (Rating BETWEEN 1 AND 10);

-- If you want to limit the length of reviews, for example, to 1000 characters, you can add the following constraint
ALTER TABLE RatingsReviews
ADD CONSTRAINT CHK_RatingsReviews_Review CHECK (CHAR_LENGTH(Review) <= 1000);














