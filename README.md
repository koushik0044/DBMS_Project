
# Movie Database Application

This README provides instructions on how to set up and run the Movie Database application, a Tkinter-based GUI application for managing a movie database.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software and how to install them:

- Python (3.x recommended)
- MySQL Server
- Any text editor (like VSCode, Sublime Text, or PyCharm)

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. **Modules Installation**:
   - Open a terminal or PowerShell in the project folder.
   - Install the required Python modules using:
     
     pip install -r requirements.txt
     

2. **Setting up the Database**:
   - Run the SQL script files in your MySQL server:
     - `project.sql`: Creates the necessary tables.
     - `constraints.sql`: Enforces constraints on the tables.
     - `triggers.sql`: Creates triggers for database operations.
     - `dummy_data.sql`: Inserts dummy records for initial setup.

3. **Configuration**:
   - In `Movie_database.py`, modify line 22 to change the `db_config` parameters to match your database settings.

4. **Initial Setup**:
   - Since there's no sign-up page, initially run:
     
     python Movie_database.py --nologin
     
     This allows you to skip the login page and create the admin account.

5. **Running the Application**:
   - After setting up the admin account, start the application with:
     
     python Movie_database.py
     
   - Log in with the admin credentials to perform CRUD operations on the movie database.

## Usage

The application provides a graphical user interface for managing a movie database. Features include adding new movies, editing existing records, and deleting movies.
