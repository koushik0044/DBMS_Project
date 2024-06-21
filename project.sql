
USE Project;

-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL, -- Should be hashed
    DateOfBirth DATE NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    INDEX (Email) -- Index on email for faster lookup
);

-- Theaters Table
CREATE TABLE Theaters (
    TheaterID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    PostalCode VARCHAR(20) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    TotalSeats INT NOT NULL,
    NumberOfScreens INT NOT NULL,
    INDEX (City), -- Useful for searching theaters by city
    INDEX (PostalCode) -- And by postal code
);

-- Movies Table
CREATE TABLE Movies (
    MovieID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Genre VARCHAR(100) NOT NULL,
    Duration INT NOT NULL,
    Director VARCHAR(255) NOT NULL,
    Cast TEXT NOT NULL,
    ReleaseDate DATE NOT NULL,
    Synopsis TEXT,
    Poster BLOB,
    INDEX (Title), -- Index on title for search operations
    INDEX (ReleaseDate) -- For filtering by release date
);

-- Screens Table
CREATE TABLE Screens (
    ScreenID INT AUTO_INCREMENT PRIMARY KEY,
    TheaterID INT NOT NULL,
    ScreenName VARCHAR(255) NOT NULL,
    SeatCapacity INT NOT NULL,
    FOREIGN KEY (TheaterID) REFERENCES Theaters(TheaterID),
    INDEX (TheaterID) -- Index on foreign key for join performance
);

-- Showtimes Table
CREATE TABLE Showtimes (
    ShowtimeID INT AUTO_INCREMENT PRIMARY KEY,
    MovieID INT NOT NULL,
    TheaterID INT NOT NULL,
    ScreenID INT NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    Date DATE NOT NULL,
    TicketPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (TheaterID) REFERENCES Theaters(TheaterID),
    FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID),
    INDEX (MovieID), -- Indexes on foreign keys for join performance
    INDEX (TheaterID),
    INDEX (Date) -- For querying showtimes by date
);

-- Tickets Table
CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    ShowtimeID INT NOT NULL,
    UserID INT,
    BookingTime DATETIME NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    SeatNumber VARCHAR(10) NOT NULL,
    FOREIGN KEY (ShowtimeID) REFERENCES Showtimes(ShowtimeID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    INDEX (ShowtimeID), -- Index for joins and searching by showtime
    INDEX (UserID) -- And by user
);

-- Payments Table
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    TicketID INT NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentStatus VARCHAR(50) NOT NULL,
    TransactionID VARCHAR(255) UNIQUE,
    FOREIGN KEY (TicketID) REFERENCES Tickets(TicketID),
    INDEX (TicketID), -- Index for join performance
    INDEX (PaymentStatus) -- For querying by payment status
);

-- Promotions Table
CREATE TABLE Promotions (
    PromoID INT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT,
    DiscountPercentage INT NOT NULL,
    ValidFrom DATE NOT NULL,
    ValidTill DATE NOT NULL,
    INDEX (Code) -- Index on promotion code for quick lookup
);

-- UserPromotions Table (Many-to-Many relationship between Users and Promotions)
CREATE TABLE UserPromotions (
    UserPromoID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    PromoID INT NOT NULL,
    DateUsed DATE NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (PromoID) REFERENCES Promotions(PromoID),
    INDEX (UserID), -- Indexes for better join performance
    INDEX (PromoID)
);

-- RatingsReviews Table
CREATE TABLE RatingsReviews (
    RatingReviewID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MovieID INT NOT NULL,
    Rating DECIMAL(2, 1) NOT NULL,
    Review TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    INDEX (UserID), -- Indexes for searching and filtering
    INDEX (MovieID),
    INDEX (Rating)
);
