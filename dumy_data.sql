Use Project;

INSERT INTO Users (FirstName, LastName, Email, Password, DateOfBirth, PhoneNumber)
VALUES
('John', 'Doe', 'john.doe@example.com', 'hashedpassword', '1990-01-15', '1234567890'),
('Alice', 'Smith', 'alice.smith@example.com', 'hashedpassword', '1985-07-22', '9876543210'),
('Bob', 'Johnson', 'bob.johnson@example.com', 'hashedpassword', '1995-04-10', '5556667777'),
('Emma', 'Davis', 'emma.davis@example.com', 'hashedpassword', '1988-09-03', '1112223333'),
('Michael', 'Williams', 'michael.williams@example.com', 'hashedpassword', '1992-12-18', '9998887777'),
('Sophia', 'Brown', 'sophia.brown@example.com', 'hashedpassword', '1980-06-25', '4443332222'),
('Ethan', 'Jones', 'ethan.jones@example.com', 'hashedpassword', '1998-03-08', '7778889999'),
('Olivia', 'Garcia', 'olivia.garcia@example.com', 'hashedpassword', '1982-11-30', '6665554444'),
('Liam', 'Martinez', 'liam.martinez@example.com', 'hashedpassword', '1993-07-12', '2223334444'),
('Ava', 'Lopez', 'ava.lopez@example.com', 'hashedpassword', '1987-05-05', '8889990000');

INSERT INTO Theaters (Name, Address, City, State, PostalCode, PhoneNumber, TotalSeats, NumberOfScreens)
VALUES
('Cineplex', '123 Main Street', 'Anytown', 'CA', '12345', '9876543210', 200, 5),
('Star Cinemas', '456 Oak Avenue', 'Cityville', 'NY', '54321', '1234567890', 150, 4),
('Grand Theaters', '789 Pine Lane', 'Townsville', 'TX', '67890', '5556667777', 180, 6),
('MegaPlex', '101 Maple Road', 'Villagetown', 'FL', '98765', '1112223333', 250, 8),
('Silver Screens', '202 Cedar Street', 'Metropolis', 'IL', '23456', '9998887777', 220, 7),
('Golden Halls', '303 Birch Boulevard', 'Hamletville', 'GA', '34567', '4443332222', 190, 5),
('Skyview Cinemas', '404 Elm Place', 'Downtown', 'CA', '45678', '7778889999', 170, 4),
('Sunset Theaters', '505 Sycamore Drive', 'Uptown', 'NY', '56789', '6665554444', 200, 6),
('City Lights Cinema', '606 Pine Avenue', 'Midtown', 'TX', '67890', '2223334444', 230, 7),
('Metro Movies', '707 Oak Lane', 'Suburbia', 'FL', '78901', '8889990000', 210, 5);

INSERT INTO Movies (Title, Genre, Duration, Director, Cast, ReleaseDate, Synopsis, Poster)
VALUES
('The Matrix', 'Sci-Fi', 150, 'Lana Wachowski', 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss', '1999-03-31', 'A hacker discovers the truth about his reality.', NULL),
('Inception', 'Sci-Fi', 148, 'Christopher Nolan', 'Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page', '2010-07-16', 'A thief enters the dreams of others to steal their secrets.', NULL),
('Titanic', 'Drama', 195, 'James Cameron', 'Leonardo DiCaprio, Kate Winslet, Billy Zane', '1997-12-19', 'A love story set against the sinking of the Titanic.', NULL),
('The Shawshank Redemption', 'Drama', 142, 'Frank Darabont', 'Tim Robbins, Morgan Freeman, Bob Gunton', '1994-09-23', 'A man is wrongly imprisoned and forms a bond with a fellow inmate.', NULL),
('The Dark Knight', 'Action', 152, 'Christopher Nolan', 'Christian Bale, Heath Ledger, Aaron Eckhart', '2008-07-18', 'Batman faces off against the Joker in Gotham City.', NULL),
('Forrest Gump', 'Drama', 142, 'Robert Zemeckis', 'Tom Hanks, Robin Wright, Gary Sinise', '1994-07-06', 'The life story of a man with a low IQ, who inadvertently influences many historical events.', NULL),
('Pulp Fiction', 'Crime', 154, 'Quentin Tarantino', 'John Travolta, Uma Thurman, Samuel L. Jackson', '1994-10-14', 'Interwoven stories of crime and redemption in Los Angeles.', NULL),
('Avatar', 'Sci-Fi', 162, 'James Cameron', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', '2009-12-18', 'A paraplegic marine is sent to the moon Pandora for a unique mission.', NULL),
('Jurassic Park', 'Adventure', 127, 'Steven Spielberg', 'Sam Neill, Laura Dern, Jeff Goldblum', '1993-06-11', 'A theme park with genetically engineered dinosaurs goes awry.', NULL),
('The Godfather', 'Crime', 175, 'Francis Ford Coppola', 'Marlon Brando, Al Pacino, James Caan', '1972-03-24', 'The patriarch of a powerful crime family hands over control to his reluctant son.', NULL);

INSERT INTO Screens (TheaterID, ScreenName, SeatCapacity)
VALUES
(1, 'Screen 1', 50),
(1, 'Screen 2', 40),
(2, 'Screen A', 60),
(2, 'Screen B', 50),
(3, 'Screen X', 55),
(3, 'Screen Y', 45),
(4, 'Screen Alpha', 70),
(4, 'Screen Beta', 60),
(5, 'Screen I', 65),
(5, 'Screen II', 55);

INSERT INTO Showtimes (MovieID, TheaterID, ScreenID, StartTime, EndTime, Date, TicketPrice)
VALUES
(1, 1, 1, '18:00:00', '21:00:00', '2023-11-15', 12.99),
(2, 2, 3, '19:30:00', '22:30:00', '2023-11-15', 14.99),
(3, 3, 5, '20:00:00', '23:00:00', '2023-11-16', 11.99),
(4, 4, 7, '17:45:00', '20:45:00', '2023-11-16', 13.99),
(5, 5, 9, '21:15:00', '23:45:00', '2023-11-17', 15.99),
(6, 6, 2, '18:30:00', '21:30:00', '2023-11-17', 12.99),
(7, 7, 4, '19:00:00', '22:00:00', '2023-11-18', 14.99),
(8, 8, 6, '20:30:00', '23:30:00', '2023-11-18', 11.99),
(9, 9, 8, '17:15:00', '20:15:00', '2023-11-19', 13.99),
(10, 10, 10, '21:45:00', '23:59:00', '2023-11-19', 15.99);


INSERT INTO Tickets (ShowtimeID, UserID, BookingTime, TotalAmount, SeatNumber)
VALUES
(31, 9, NOW(), 12.99, 'A10'),
(32, 10, NOW(), 14.99, 'B20'),
(33, 11, NOW(), 11.99, 'X15'),
(34, 12, NOW(), 13.99, 'Alpha25'),
(35, 13, NOW(), 15.99, 'I30'),
(36, 14, NOW(), 12.99, '2B'),
(37, 15, NOW(), 14.99, 'Alpha12'),
(38, 16, NOW(), 11.99, 'I22'),
(39, 17, NOW(), 13.99, 'X10'),
(40, 18, NOW(), 15.99, 'Beta18');


INSERT INTO Payments (TicketID, PaymentMethod, Amount, PaymentStatus, TransactionID)
VALUES
(21, 'Credit Card', 12.99, 'Completed', 'XYZ123'),
(22, 'PayPal', 14.99, 'Pending', NULL),
(23, 'Credit Card', 11.99, 'Completed', 'ABC456'),
(24, 'Bank Transfer', 13.99, 'Failed', NULL),
(25, 'Credit Card', 15.99, 'Completed', 'DEF789'),
(26, 'PayPal', 12.99, 'Completed', 'GHI101'),
(27, 'Credit Card', 14.99, 'Pending', NULL),
(28, 'Bank Transfer', 11.99, 'Completed', 'JKL111'),
(29, 'Credit Card', 13.99, 'Failed', NULL),
(30, 'PayPal', 15.99, 'Completed', 'MNO121');


INSERT INTO Promotions (Code, Description, DiscountPercentage, ValidFrom, ValidTill)
VALUES
('SUMMER20', '20% off for the summer', 20, '2023-06-01', '2023-08-31'),
('FAMILY50', '50% off for family tickets', 50, '2023-01-01', '2023-12-31'),
('EARLYBIRD10', '10% off for early morning shows', 10, '2023-11-15', '2023-11-30'),
('WEEKEND25', '25% off for weekend screenings', 25, '2023-11-18', '2023-11-20'),
('LOYALTY15', '15% off for loyal customers', 15, '2023-01-01', '2023-12-31'),
('STUDENTDISC', 'Special discount for students', 30, '2023-01-01', '2023-12-31'),
('HOLIDAY10', '10% off for the holidays', 10, '2023-12-01', '2023-12-31'),
('BIRTHDAYFREE', 'Free ticket on your birthday', 100, '2023-01-01', '2023-12-31'),
('GROUP30', '30% off for group bookings', 30, '2023-01-01', '2023-12-31'),
('VETERAN20', '20% off for veterans', 20, '2023-11-11', '2023-11-12');


INSERT INTO UserPromotions (UserID, PromoID, DateUsed)
VALUES
(9, 31, '2023-06-10'),
(10, 32, '2023-07-05'),
(11, 33, '2023-11-20'),
(12, 34, '2023-11-25'),
(13, 35, '2023-02-15'),
(14, 36, '2023-09-08'),
(15, 37, '2023-11-18'),
(16, 38, '2023-04-30'),
(17, 39, '2023-11-05'),
(18, 40, '2023-11-11');


INSERT INTO RatingsReviews (UserID, MovieID, Rating, Review)
VALUES
(9, 1, 4.5, 'Great movie, loved the action scenes.'),
(10, 2, 5.0, 'Mind-bending plot, exceptional visual effects.'),
(11, 3, 3.5, 'Classic romance, but a bit too long.'),
(12, 4, 4.0, 'Inspirational and powerful.'),
(13, 5, 4.8, 'Heath Ledgers Joker is iconic.'),
(14, 6, 4.2, 'Heartwarming and emotionally powerful.'),
(15, 7, 4.7, 'Quentin Tarantinos masterpiece.'),
(16, 8, 3.8, 'Visually stunning but a bit slow.'),
(17, 9, 4.5, 'Dinosaurs never get old.'),
(18, 10, 4.0, 'A cinematic masterpiece, captivating storyline.');


