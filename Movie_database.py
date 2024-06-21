import tkinter as tk
from tkinter import ttk, messagebox, font ,filedialog
import mysql.connector
from mysql.connector import Error
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--nologin', action='store_true', help='Skip login page')
args = parser.parse_args()

# Function to clear the entry fields
def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database connection parameters - SHOULD BE STORED SECURELY
db_config = {
    'host': 'localhost',
    'user': 'root',  # replace with your MySQL username
    'password': 'koushik04',  # replace with your MySQL password
    'database': 'Project'  # replace with your database name
}

# Establish a MySQL database connection
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        messagebox.showerror("Database Connection Error", f"Error: '{e}'")
        return None

# Execute a generic database query with error handling
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        messagebox.showerror("Database Query Error", f"Error: '{e}'")
        return False


# Function to verify admin login
def verify_admin_login(email, password, root):
    connection = create_connection()
    if connection:
        hashed_password = hash_password(password)
        cursor = connection.cursor(buffered=True)
        query = "SELECT isAdmin FROM Users WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()
        if result and result[0]:
            # If the login is successful and the user is an admin
            cursor.close()
            connection.close()
            root.deiconify()  # Show the main window if login is successful
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or not an admin.")
            cursor.close()
            connection.close()
            root.destroy()  # Close the application if login fails

# Function to create the login window
def create_login_window():
    login_window = tk.Toplevel()
    login_window.title("Admin Login")

    # Email Entry
    email_label = ttk.Label(login_window, text="Email:")
    email_label.grid(row=0, column=0, padx=10, pady=10)
    email_entry = ttk.Entry(login_window)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password Entry
    password_label = ttk.Label(login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login Button
    login_button = ttk.Button(login_window, text="Login", command=lambda: verify_admin_login(email_entry.get(), password_entry.get(), root))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    return login_window



# Function to insert a new user
def insert_user(entries, is_admin_var,users_tree):
    connection = create_connection()
    if connection:
        hashed_password = hash_password(entries[-1].get())
        query = """
        INSERT INTO Users (FirstName, LastName, Email, DateOfBirth, PhoneNumber, Password, isAdmin) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in entries[:-1]) + (hashed_password, is_admin_var.get(),)
        if execute_query(connection, query, data):
            clear_entries(entries)
            is_admin_var.set(False)  # Reset the isAdmin checkbox
            populate_treeview(users_tree)  # Refresh the treeview
            messagebox.showinfo("Success", "User added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add user.")
        connection.close()


def update_user(entries, user_id, is_admin_var,users_tree):
    connection = create_connection()
    if connection and user_id.isdigit():
        user_id = int(user_id)
        
        # Create a dictionary of column names and entry widgets, without the password field
        fields = {
            "FirstName": entries[0].get(),
            "LastName": entries[1].get(),
            "Email": entries[2].get(),
            "DateOfBirth": entries[3].get(),
            "PhoneNumber": entries[4].get()
        }
        
        # Start building the SQL update query
        update_parts = []
        data = []

        # Add non-empty fields to the update query
        for field_name, value in fields.items():
            if value:
                update_parts.append(f"{field_name} = %s")
                data.append(value)
        
        # Check if the password field is non-empty and hash the new password
        if entries[5].get():
            update_parts.append("Password = %s")
            hashed_password = hash_password(entries[5].get())
            data.append(hashed_password)

        # Add isAdmin field to the update query
        update_parts.append("isAdmin = %s")
        data.append(is_admin_var.get())

        # Finalize the update query
        set_clause = ", ".join(update_parts)
        data.append(user_id)  # Append the UserID at the end of the data list

        query = f"UPDATE Users SET {set_clause} WHERE UserID = %s"

        if execute_query(connection, query, data):
            clear_entries(entries)
            is_admin_var.set(False)  # Reset the isAdmin checkbox
            populate_treeview(users_tree)  # Refresh the treeview
            messagebox.showinfo("Success", "User updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update user.")

        connection.close()
    else:
        messagebox.showerror("Error", "Invalid UserID provided.")


# Function to delete a user
def delete_user(user_id,users_tree):
    if not user_id:
        messagebox.showerror("Error", "UserID is required to delete a user.")
        return
    
    response = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
    if response:
        connection = create_connection()
        if connection:
            query = "DELETE FROM Users WHERE UserID = %s"
            if execute_query(connection, query, (user_id,)):
                populate_treeview(users_tree)  # Refresh the treeview
                messagebox.showinfo("Success", "User deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete user.")
            connection.close()

def display_all_users(users_tree):
    # Clear existing Treeview entries
    for item in users_tree.get_children():
        users_tree.delete(item)
    
    # Establish a database connection
    connection = create_connection()
    if connection:
        # Query to select all user data
        query = "SELECT UserID, FirstName, LastName, Email, DateOfBirth, PhoneNumber, isAdmin FROM Users"
        users = execute_read_query(connection, query)
        if users:
            # Insert each user into the Treeview
            for user in users:
                # Format isAdmin as 'Yes' or 'No' for display
                formatted_user = user[:-1] + ("Yes" if user[-1] else "No",)
                users_tree.insert('', 'end', values=formatted_user)
        connection.close()

# Function to populate the treeview with database data
def populate_treeview(users_tree):
    # Clear existing treeview entries
    for item in users_tree.get_children():
        users_tree.delete(item)
    
    # Establish database connection
    connection = create_connection()
    if connection:
        # Query to select data including isAdmin column
        query = "SELECT UserID, FirstName, LastName, Email, DateOfBirth, PhoneNumber, isAdmin FROM Users"
        users = execute_read_query(connection, query)
        if users:
            # Insert data into treeview
            for user in users:
                # Format isAdmin as 'Yes' or 'No' for display
                formatted_user = user[:-1] + ("Yes" if user[-1] else "No",)
                users_tree.insert('', 'end', values=formatted_user)
        connection.close()

# Function to insert a new theater into the database
def insert_theater(entries,theaters_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Theaters (Name, Address, City, State, PostalCode, PhoneNumber, TotalSeats, NumberOfScreens) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in entries)
        if execute_query(connection, query, data):
            clear_entries(entries)
            display_all_theaters(theaters_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Theater added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add theater.")
        connection.close()

# Function to update an existing theater in the database
def update_theater(entries, theater_id, theaters_tree):
    connection = create_connection()
    if connection and theater_id.isdigit():
        theater_id = int(theater_id)
        query_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["Name", "Address", "City", "State", "PostalCode", "PhoneNumber", "TotalSeats", "NumberOfScreens"]
        
        # Build the query dynamically based on the non-empty entries
        for entry, col in zip(entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                query_parts.append(f"{col} = %s")
                data.append(value)

        # If there are no fields to update, we don't execute the query
        if not query_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return

        # Complete the query with the provided parts
        query = "UPDATE Theaters SET " + ", ".join(query_parts) + " WHERE TheaterID = %s"
        data.append(theater_id)  # Add the theater_id to the data tuple
        
        if execute_query(connection, query, data):
            clear_entries(entries)  # Assuming clear_entries is designed to clear the fields
            display_all_theaters(theaters_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Theater updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update theater.")
        connection.close()
    else:
        messagebox.showerror("Error", "Invalid TheaterID provided.")

# Function to delete a theater from the database
def delete_theater(theater_id,theaters_tree):
    if not theater_id:
        messagebox.showerror("Error", "TheaterID is required to delete a theater.")
        return
    response = messagebox.askyesno("Confirm", "Are you sure you want to delete this theater?")
    if response:
        connection = create_connection()
        if connection:
            query = "DELETE FROM Theaters WHERE TheaterID = %s"
            if execute_query(connection, query, (theater_id,)):
                display_all_theaters(theaters_tree)  # Refresh the Treeview
                messagebox.showinfo("Success", "Theater deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete theater.")
            connection.close()

# Function to fetch and display all theaters in the Treeview
def display_all_theaters(theaters_tree):
    # Clear existing Treeview entries
    for item in theaters_tree.get_children():
        theaters_tree.delete(item)
    
    # Establish database connection
    connection = create_connection()
    if connection:
        query = "SELECT TheaterID, Name, Address, City, State, PostalCode, PhoneNumber, TotalSeats, NumberOfScreens FROM Theaters"
        theaters = execute_read_query(connection, query)
        if theaters:
            # Insert each theater into the Treeview
            for theater in theaters:
                theaters_tree.insert('', 'end', values=theater)
        connection.close()

def insert_movie(entries,movies_tree):
    connection = create_connection()
    if connection:
        synopsis_text = entries[-2].get("1.0", tk.END).strip()  # Get text from Text widget for Synopsis
        poster_path = entries[-1].get()  # Get the file path from the Entry widget for Poster

        # Initialize data tuple with values from Entry widgets, exclude 'Synopsis' and 'Poster'
        data = tuple(entry.get() for entry in entries[:-2])

        # Add 'Synopsis' text to the data tuple
        data += (synopsis_text,)

        # Handle 'Poster' if a path has been provided, else add None
        blob_data = None
        if poster_path:
            try:
                with open(poster_path, 'rb') as file:
                    blob_data = file.read()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read poster image: {e}")
                return
        data += (blob_data,)

        # Construct the SQL query with the right number of placeholders
        query = """
        INSERT INTO Movies (Title, Genre, Duration, Director, Cast, ReleaseDate, Synopsis, Poster) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Execute the query with the data tuple
        if execute_query(connection, query, data):
            for entry in entries:
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, tk.Text):
                    entry.delete("1.0", tk.END)  # Assuming you have a way to clear all entries
            messagebox.showinfo("Success", "Movie added successfully!")
            display_all_movies(movies_tree)  # Refresh the Treeview
        else:
            messagebox.showerror("Error", "Failed to add movie.")
        connection.close()


def update_movie(entries, movie_id, movies_tree):
    connection = create_connection()
    if connection and movie_id.isdigit():
        movie_id = int(movie_id)
        update_parts = []
        data = []

        # Corresponding column names in the database
        column_names = ["Title", "Genre", "Duration", "Director", "Cast", "ReleaseDate"]

        # Build the update_parts and data for non-empty entries
        for entry, column_name in zip(entries[:-2], column_names):  # Exclude the last two (Synopsis and Poster)
            value = entry.get()
            if value:  # Check if the entry has a value
                update_parts.append(f"{column_name} = %s")
                data.append(value)

        # Handle the 'Synopsis' which uses a Text widget
        synopsis_text = entries[-2].get("1.0", tk.END).strip()
        if synopsis_text:
            update_parts.append("Synopsis = %s")
            data.append(synopsis_text)

        # Handle the 'Poster' path, convert to binary if provided
        poster_path = entries[-1].get()
        if poster_path:  # Only update if a path is provided
            try:
                with open(poster_path, 'rb') as file:
                    blob_data = file.read()
                update_parts.append("Poster = %s")
                data.append(blob_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read poster image: {e}")
                return

        # Append the MovieID at the end of the data list
        data.append(movie_id)

        # If no update parts were added, then there's nothing to update
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            connection.close()
            return

        # Construct and execute the update query
        query = "UPDATE Movies SET " + ", ".join(update_parts) + " WHERE MovieID = %s"
        if execute_query(connection, query, tuple(data)):
            messagebox.showinfo("Success", "Movie updated successfully!")
            display_all_movies(movies_tree)  # Refresh the Treeview
        else:
            messagebox.showerror("Error", "Failed to update movie.")
        connection.close()
    else:
        messagebox.showerror("Error", "Invalid MovieID provided.")


def delete_movie(movie_id, movies_tree):
    if not movie_id:
        messagebox.showerror("Error", "MovieID is required to delete a movie.")
        return
    
    response = messagebox.askyesno("Confirm", "Are you sure you want to delete this movie?")
    if response:
        connection = create_connection()
        if connection:
            query = "DELETE FROM Movies WHERE MovieID = %s"
            if execute_query(connection, query, (movie_id,)):
                messagebox.showinfo("Success", "Movie deleted successfully!")
                display_all_movies(movies_tree)  # Refresh the Treeview
            else:
                messagebox.showerror("Error", "Failed to delete movie.")
            connection.close()

def display_all_movies(movies_tree):
    for item in movies_tree.get_children():
        movies_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT MovieID, Title, Genre, Duration, Director, Cast, ReleaseDate, Synopsis FROM Movies"
        movies = execute_read_query(connection, query)
        if movies:
            for movie in movies:
                movies_tree.insert('', 'end', values=movie)
        connection.close()

def select_poster_file(entry):
    file_path = filedialog.askopenfilename(
        title="Select a poster image file",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All files", "*.*")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def insert_screen(screen_entries,screens_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Screens (TheaterID, ScreenName, SeatCapacity) 
        VALUES (%s, %s, %s)
        """
        data = (screen_entries[0].get(), screen_entries[1].get(), screen_entries[2].get())
        if execute_query(connection, query, data):
            for entry in screen_entries:
                entry.delete(0, tk.END)
            display_all_screens(screens_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Screen added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add screen.")
        connection.close()

def update_screen(screen_entries, screen_id, screens_tree):
    connection = create_connection()
    if connection and screen_id.isdigit():
        screen_id = int(screen_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["TheaterID", "ScreenName", "SeatCapacity"]
        
        # Build the query dynamically based on non-empty fields
        for entry, col in zip(screen_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)
        
        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return
        
        # Append the ScreenID to the data list
        data.append(screen_id)
        
        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE Screens SET {set_clause} WHERE ScreenID = %s"
        
        if execute_query(connection, query, data):
            clear_entries(screen_entries)  # Assuming you have a way to clear all entries
            display_all_screens(screens_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Screen updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update screen.")
        connection.close()

def delete_screen(screen_id, screens_tree):
    connection = create_connection()
    if connection:
        query = "DELETE FROM Screens WHERE ScreenID = %s"
        if execute_query(connection, query, (screen_id,)):
            display_all_screens(screens_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Screen deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete screen.")
        connection.close()

def display_all_screens(screens_tree):
    for item in screens_tree.get_children():
        screens_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT ScreenID, TheaterID, ScreenName, SeatCapacity FROM Screens"
        screens = execute_read_query(connection, query)
        if screens:
            for screen in screens:
                screens_tree.insert('', 'end', values=screen)
        connection.close()

def insert_showtime(showtime_entries, showtimes_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Showtimes (MovieID, TheaterID, ScreenID, StartTime, EndTime, Date, TicketPrice) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in showtime_entries)
        if execute_query(connection, query, data):
            for entry in showtime_entries:
                entry.delete(0, tk.END)
            display_all_showtimes(showtimes_tree)
            messagebox.showinfo("Success", "Showtime added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add showtime.")
        connection.close()

def update_showtime(showtime_entries, showtime_id, showtimes_tree):
    connection = create_connection()
    if connection and showtime_id.isdigit():
        showtime_id = int(showtime_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["MovieID", "TheaterID", "ScreenID", "StartTime", "EndTime", "Date", "TicketPrice"]
        
        # Build the query dynamically based on non-empty fields
        for entry, col in zip(showtime_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)
        
        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return
        
        # Append the ShowtimeID to the data list
        data.append(showtime_id)
        
        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE Showtimes SET {set_clause} WHERE ShowtimeID = %s"
        
        if execute_query(connection, query, data):
            clear_entries(showtime_entries)  # Assuming you have a way to clear all entries
            display_all_showtimes(showtimes_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Showtime updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update showtime.")
        connection.close()

def delete_showtime(showtime_id, showtimes_tree):
    connection = create_connection()
    if connection:
        query = "DELETE FROM Showtimes WHERE ShowtimeID = %s"
        if execute_query(connection, query, (showtime_id,)):
            display_all_showtimes(showtimes_tree)
            messagebox.showinfo("Success", "Showtime deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete showtime.")
        connection.close()

def display_all_showtimes(showtimes_tree):
    for item in showtimes_tree.get_children():
        showtimes_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT ShowtimeID, MovieID, TheaterID, ScreenID, StartTime, EndTime, Date, TicketPrice FROM Showtimes"
        showtimes = execute_read_query(connection, query)
        if showtimes:
            for showtime in showtimes:
                showtimes_tree.insert('', 'end', values=showtime)
        connection.close()

def insert_ticket(ticket_entries, tickets_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Tickets (ShowtimeID, UserID, BookingTime, TotalAmount, SeatNumber) 
        VALUES (%s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in ticket_entries)
        if execute_query(connection, query, data):
            for entry in ticket_entries:
                entry.delete(0, tk.END)
            display_all_tickets(tickets_tree)
            messagebox.showinfo("Success", "Ticket added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add ticket.")
        connection.close()

def update_ticket(ticket_entries, ticket_id, tickets_tree):
    connection = create_connection()
    if connection and ticket_id.isdigit():
        ticket_id = int(ticket_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["ShowtimeID", "UserID", "BookingTime", "TotalAmount", "SeatNumber"]

        # Build the query dynamically based on non-empty fields
        for entry, col in zip(ticket_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)

        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return

        # Append the TicketID to the data list
        data.append(ticket_id)

        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE Tickets SET {set_clause} WHERE TicketID = %s"

        if execute_query(connection, query, data):
            clear_entries(ticket_entries)
            display_all_tickets(tickets_tree)
            messagebox.showinfo("Success", "Ticket updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update ticket.")
        connection.close()

def delete_ticket(ticket_id, tickets_tree):
    connection = create_connection()
    if connection and ticket_id.isdigit():
        query = "DELETE FROM Tickets WHERE TicketID = %s"
        if execute_query(connection, query, (ticket_id,)):
            display_all_tickets(tickets_tree)
            messagebox.showinfo("Success", "Ticket deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete ticket.")
        connection.close()

def display_all_tickets(tickets_tree):
    for item in tickets_tree.get_children():
        tickets_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT TicketID, ShowtimeID, UserID, BookingTime, TotalAmount, SeatNumber FROM Tickets"
        tickets = execute_read_query(connection, query)
        if tickets:
            for ticket in tickets:
                tickets_tree.insert('', 'end', values=ticket)
        connection.close()

def insert_payment(payment_entries, payments_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Payments (TicketID, PaymentMethod, Amount, PaymentStatus, TransactionID) 
        VALUES (%s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in payment_entries)
        if execute_query(connection, query, data):
            for entry in payment_entries:
                entry.delete(0, tk.END)
            display_all_payments(payments_tree)
            messagebox.showinfo("Success", "Payment added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add payment.")
        connection.close()

def update_payment(payment_entries, payment_id, payments_tree):
    connection = create_connection()
    if connection and payment_id.isdigit():
        payment_id = int(payment_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["TicketID", "PaymentMethod", "Amount", "PaymentStatus", "TransactionID"]

        # Build the query dynamically based on non-empty fields
        for entry, col in zip(payment_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)

        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return

        # Append the PaymentID to the data list
        data.append(payment_id)

        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE Payments SET {set_clause} WHERE PaymentID = %s"

        if execute_query(connection, query, data):
            clear_entries(payment_entries)
            display_all_payments(payments_tree)
            messagebox.showinfo("Success", "Payment updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update payment.")
        connection.close()

def delete_payment(payment_id, payments_tree):
    connection = create_connection()
    if connection and payment_id.isdigit():
        query = "DELETE FROM Payments WHERE PaymentID = %s"
        if execute_query(connection, query, (payment_id,)):
            display_all_payments(payments_tree)
            messagebox.showinfo("Success", "Payment deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete payment.")
        connection.close()

def display_all_payments(payments_tree):
    for item in payments_tree.get_children():
        payments_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT PaymentID, TicketID, PaymentMethod, Amount, PaymentStatus, TransactionID FROM Payments"
        payments = execute_read_query(connection, query)
        if payments:
            for payment in payments:
                payments_tree.insert('', 'end', values=payment)
        connection.close()

def insert_promotion(promotion_entries, promotions_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO Promotions (Code, Description, DiscountPercentage, ValidFrom, ValidTill) 
        VALUES (%s, %s, %s, %s, %s)
        """
        data = tuple(entry.get() for entry in promotion_entries)
        if execute_query(connection, query, data):
            for entry in promotion_entries:
                entry.delete(0, tk.END)
            display_all_promotions(promotions_tree)
            messagebox.showinfo("Success", "Promotion added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add promotion.")
        connection.close()

def update_promotion(promotion_entries, promo_id, promotions_tree):
    connection = create_connection()
    if connection and promo_id.isdigit():
        promo_id = int(promo_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["Code", "Description", "DiscountPercentage", "ValidFrom", "ValidTill"]

        # Build the query dynamically based on non-empty fields
        for entry, col in zip(promotion_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)

        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return

        # Append the PromoID to the data list
        data.append(promo_id)

        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE Promotions SET {set_clause} WHERE PromoID = %s"

        if execute_query(connection, query, data):
            clear_entries(promotion_entries)
            display_all_promotions(promotions_tree)
            messagebox.showinfo("Success", "Promotion updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update promotion.")
        connection.close()

def delete_promotion(promo_id, promotions_tree):
    connection = create_connection()
    if connection and promo_id.isdigit():
        query = "DELETE FROM Promotions WHERE PromoID = %s"
        if execute_query(connection, query, (promo_id,)):
            display_all_promotions(promotions_tree)
            messagebox.showinfo("Success", "Promotion deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete promotion.")
        connection.close()

def display_all_promotions(promotions_tree):
    for item in promotions_tree.get_children():
        promotions_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT PromoID, Code, Description, DiscountPercentage, ValidFrom, ValidTill FROM Promotions"
        promotions = execute_read_query(connection, query)
        if promotions:
            for promotion in promotions:
                promotions_tree.insert('', 'end', values=promotion)
        connection.close()

def insert_user_promotion(user_promotion_entries, user_promotions_tree):
    connection = create_connection()
    if connection:
        query = """
        INSERT INTO UserPromotions (UserID, PromoID, DateUsed) 
        VALUES (%s, %s, %s)
        """
        data = tuple(entry.get() for entry in user_promotion_entries)
        if execute_query(connection, query, data):
            for entry in user_promotion_entries:
                entry.delete(0, tk.END)
            display_all_user_promotions(user_promotions_tree)
            messagebox.showinfo("Success", "User Promotion added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add User Promotion.")
        connection.close()

def update_user_promotion(user_promotion_entries, user_promo_id, user_promotions_tree):
    connection = create_connection()
    if connection and user_promo_id.isdigit():
        user_promo_id = int(user_promo_id)
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["UserID", "PromoID", "DateUsed"]

        # Build the query dynamically based on non-empty fields
        for entry, col in zip(user_promotion_entries, columns):
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)

        # If no fields were modified, inform the user and exit the function
        if not update_parts:
            messagebox.showinfo("No Changes", "No fields were modified.")
            return

        # Append the UserPromoID to the data list
        data.append(user_promo_id)

        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE UserPromotions SET {set_clause} WHERE UserPromoID = %s"

        if execute_query(connection, query, data):
            clear_entries(user_promotion_entries)
            display_all_user_promotions(user_promotions_tree)
            messagebox.showinfo("Success", "User Promotion updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update User Promotion.")
        connection.close()

def delete_user_promotion(user_promo_id, user_promotions_tree):
    connection = create_connection()
    if connection and user_promo_id.isdigit():
        query = "DELETE FROM UserPromotions WHERE UserPromoID = %s"
        if execute_query(connection, query, (user_promo_id,)):
            display_all_user_promotions(user_promotions_tree)
            messagebox.showinfo("Success", "User Promotion deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete User Promotion.")
        connection.close()

def display_all_user_promotions(user_promotions_tree):
    for item in user_promotions_tree.get_children():
        user_promotions_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT UserPromoID, UserID, PromoID, DateUsed FROM UserPromotions"
        user_promotions = execute_read_query(connection, query)
        if user_promotions:
            for user_promotion in user_promotions:
                user_promotions_tree.insert('', 'end', values=user_promotion)
        connection.close()

def insert_rating_review(rating_review_entries, ratings_reviews_tree):
    connection = create_connection()
    if connection:
        review_text = rating_review_entries[-1].get("1.0", tk.END).strip()  # Assuming the last entry is the review Text widget
        query = """
        INSERT INTO RatingsReviews (UserID, MovieID, Rating, Review) 
        VALUES (%s, %s, %s, %s)
        """
        data = tuple(entry.get() if i < len(rating_review_entries) - 1 else review_text for i, entry in enumerate(rating_review_entries))
        if execute_query(connection, query, data):
            for entry in rating_review_entries:
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, tk.Text):
                    entry.delete("1.0", tk.END)
            display_all_ratings_reviews(ratings_reviews_tree)
            messagebox.showinfo("Success", "Rating/Review added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add Rating/Review.")
        connection.close()

def update_rating_review(rating_review_entries, rating_review_id, ratings_reviews_tree):
    connection = create_connection()
    if connection and rating_review_id.isdigit():
        rating_review_id = int(rating_review_id)
        review_text = rating_review_entries[-1].get("1.0", tk.END).strip()  # Last entry is the review Text widget
        update_parts = []
        data = []

        # List of column names in the same order as the entries
        columns = ["UserID", "MovieID", "Rating", "Review"]

        # Build the query dynamically based on non-empty fields
        for entry, col in zip(rating_review_entries[:-1], columns[:-1]):  # Exclude the review Text widget
            value = entry.get()
            if value:  # Only include non-empty fields in the update
                update_parts.append(f"{col} = %s")
                data.append(value)
        
        # Always include the review text in the update
        update_parts.append("Review = %s")
        data.append(review_text)

        # Append the RatingReviewID to the data list
        data.append(rating_review_id)

        # Construct the SQL command
        set_clause = ", ".join(update_parts)
        query = f"UPDATE RatingsReviews SET {set_clause} WHERE RatingReviewID = %s"

        if execute_query(connection, query, data):
            clear_entries(rating_review_entries)  # Clear all fields
            display_all_ratings_reviews(ratings_reviews_tree)  # Refresh the Treeview
            messagebox.showinfo("Success", "Rating/Review updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update Rating/Review.")
        connection.close()

def delete_rating_review(rating_review_id, ratings_reviews_tree):
    connection = create_connection()
    if connection and rating_review_id.isdigit():
        query = "DELETE FROM RatingsReviews WHERE RatingReviewID = %s"
        if execute_query(connection, query, (rating_review_id,)):
            display_all_ratings_reviews(ratings_reviews_tree)
            messagebox.showinfo("Success", "Rating/Review deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete Rating/Review.")
        connection.close()

def display_all_ratings_reviews(ratings_reviews_tree):
    for item in ratings_reviews_tree.get_children():
        ratings_reviews_tree.delete(item)
    
    connection = create_connection()
    if connection:
        query = "SELECT RatingReviewID, UserID, MovieID, Rating, Review FROM RatingsReviews"
        rating_reviews = execute_read_query(connection, query)
        if rating_reviews:
            for rating_review in rating_reviews:
                # Truncate review text for display if necessary
                display_text = (rating_review[4][:75] + '...') if len(rating_review[4]) > 75 else rating_review[4]
                ratings_reviews_tree.insert('', 'end', values=(rating_review[0], rating_review[1], rating_review[2], rating_review[3], display_text))
        connection.close()


# Function to execute a read query
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Error: '{e}'")
    return result

def create_users_tab(notebook):
    users_tab = ttk.Frame(notebook)
    notebook.add(users_tab, text='Users')
    # Entry fields for user data
    labels = ["First Name", "Last Name", "Email", "Date of Birth (YYYY-MM-DD)", "Phone Number", "Password"]
    is_admin_var = tk.BooleanVar(value=False)
    entries = []
    for i, label in enumerate(labels):
        lbl = ttk.Label(users_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(users_tab, show="*" if label == "Password" else None)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        entries.append(entry)
    admin_label = ttk.Label(users_tab, text="Is Admin:")
    admin_label.grid(row=len(labels), column=0, padx=10, pady=10, sticky='W')
    admin_checkbox = ttk.Checkbutton(users_tab, text="Check if user is an admin", variable=is_admin_var)
    admin_checkbox.grid(row=len(labels), column=1, padx=10, pady=10, sticky='W')
    
    button_start_row = len(labels) + 2

# Button to insert a new user
    insert_button = ttk.Button(users_tab, text="Insert User", command=lambda: insert_user(entries, is_admin_var,users_tree))
    insert_button.grid(row=button_start_row, column=0, padx=10, pady=10, sticky='W')

    # Entry field for UserID (for update and delete operations)
    user_id_label = ttk.Label(users_tab, text="UserID")
    user_id_label.grid(row=7, column=0, padx=10, pady=10, sticky='W')
    user_id_entry = ttk.Entry(users_tab)
    user_id_entry.grid(row=7, column=1, padx=10, pady=10, sticky='W')

    # Button to update an existing user
    update_button = ttk.Button(users_tab, text="Update User", command=lambda: update_user(entries, user_id_entry.get(),is_admin_var,users_tree))
    update_button.grid(row=button_start_row, column=1, padx=10, pady=10, sticky='W')

    # Button to delete a user
    delete_button = ttk.Button(users_tab, text="Delete User", command=lambda: delete_user(user_id_entry.get(),users_tree))
    delete_button.grid(row=button_start_row + 1, column=0, padx=10, pady=10, sticky='W')

    columns = ("UserID", "FirstName", "LastName", "Email", "DateOfBirth", "PhoneNumber", "Is Admin")
    users_tree = ttk.Treeview(users_tab, columns=columns, show='headings', height=8)

    display_all_btn = ttk.Button(users_tab, text="Display All Users", command=display_all_users(users_tree))
    display_all_btn.grid(row=button_start_row + 3, column=0, padx=10, pady=10, sticky='W')

    for col in columns:
        users_tree.heading(col, text=col.replace("_", " "))
        users_tree.column(col, anchor='w')  # Set the alignment to west/left

    # Set the width of the columns to fit the column title
    font_obj = font.Font()
    for col in columns:
        width = font_obj.measure(col.title()) + 10  # Add some padding
        users_tree.column(col, width=width, minwidth=width)

    # Add data to the treeview
    populate_treeview(users_tree)

    # Create Treeview to show the Users
    users_tree.grid(row=button_start_row + 2, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Configure the grid to allow the Treeview to resize with the window
    users_tab.grid_rowconfigure(button_start_row + 2, weight=1)
    users_tab.grid_columnconfigure(1, weight=1)
    
    return users_tab

# Function to create the Theaters tab
def create_theaters_tab(notebook):
    theaters_tab = ttk.Frame(notebook)
    notebook.add(theaters_tab, text='Theaters')
    
    # Entry fields for theater data
    theater_labels = ["Name", "Address", "City", "State", "PostalCode", "PhoneNumber", "TotalSeats", "NumberOfScreens"]
    theater_entries = []
    # Treeview for Theaters
    theater_columns = ("TheaterID", "Name", "Address", "City", "State", "PostalCode", "PhoneNumber", "TotalSeats", "NumberOfScreens")
    theaters_tree = ttk.Treeview(theaters_tab, columns=theater_columns, show='headings', height=8)

    for i, label in enumerate(theater_labels):
        lbl = ttk.Label(theaters_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(theaters_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        theater_entries.append(entry)

    # TheaterID field for update and delete operations
    theater_id_label = ttk.Label(theaters_tab, text="TheaterID")
    theater_id_label.grid(row=len(theater_labels), column=0, padx=10, pady=10, sticky='W')
    theater_id_entry = ttk.Entry(theaters_tab)
    theater_id_entry.grid(row=len(theater_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_theater_button = ttk.Button(theaters_tab, text="Insert Theater", command=lambda: insert_theater(theater_entries,theaters_tree))
    insert_theater_button.grid(row=len(theater_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_theater_button = ttk.Button(theaters_tab, text="Update Theater", command=lambda: update_theater(theater_entries, theater_id_entry.get(),theaters_tree))
    update_theater_button.grid(row=len(theater_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_theater_button = ttk.Button(theaters_tab, text="Delete Theater", command=lambda: delete_theater(theater_id_entry.get(),theaters_tree))
    delete_theater_button.grid(row=len(theater_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_theaters_button = ttk.Button(theaters_tab, text="Display All Theaters", command=lambda: display_all_theaters(theaters_tree))
    display_all_theaters_button.grid(row=len(theater_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    for col in theater_columns:
        theaters_tree.heading(col, text=col.replace("_", " "))
        theaters_tree.column(col, anchor='w', width= 100)

    theaters_tree.grid(row=len(theater_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbar for the Treeview
    theater_scrollbar = ttk.Scrollbar(theaters_tab, orient='vertical', command=theaters_tree.yview)
    theater_scrollbar.grid(row=len(theater_labels) + 3, column=2, sticky='ns')
    theaters_tree.configure(yscroll=theater_scrollbar.set)

    # You would define the insert_theater, update_theater, delete_theater, and display_all_theaters functions
    # These functions would interact with the database to perform the respective operations

    return theaters_tab

# Function to create the Movies tab
def create_movies_tab(notebook):
    movies_tab = ttk.Frame(notebook)
    notebook.add(movies_tab, text='Movies')
    
    # Entry fields for movie data
    movie_labels = ["Title", "Genre", "Duration", "Director", "Cast", "ReleaseDate", "Synopsis", "Poster"]
    movie_entries = []
    # Treeview for Movies
    movie_columns = ("MovieID", "Title", "Genre", "Duration", "Director", "Cast", "ReleaseDate", "Synopsis", "Poster")
    movies_tree = ttk.Treeview(movies_tab, columns=movie_columns, show='headings', height=8)

    for i, label in enumerate(movie_labels):
        lbl = ttk.Label(movies_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(movies_tab)
        if label == "Synopsis":  # Make Synopsis entry larger
            entry = tk.Text(movies_tab, height=4, width=50)
        elif label == "Poster":  # Allow only file path entry for Poster
            browse_button = ttk.Button(movies_tab, text="Browse...", command=lambda e=entry: select_poster_file(e))
            browse_button.grid(row=i, column=2, padx=10, pady=10)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        movie_entries.append(entry)

    # MovieID field for update and delete operations
    movie_id_label = ttk.Label(movies_tab, text="MovieID")
    movie_id_label.grid(row=len(movie_labels), column=0, padx=10, pady=10, sticky='W')
    movie_id_entry = ttk.Entry(movies_tab)
    movie_id_entry.grid(row=len(movie_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_movie_button = ttk.Button(movies_tab, text="Insert Movie", command=lambda: insert_movie(movie_entries,movies_tree))
    insert_movie_button.grid(row=len(movie_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_movie_button = ttk.Button(movies_tab, text="Update Movie", command=lambda: update_movie(movie_entries, movie_id_entry.get(),movies_tree))
    update_movie_button.grid(row=len(movie_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_movie_button = ttk.Button(movies_tab, text="Delete Movie", command=lambda: delete_movie(movie_id_entry.get(),movies_tree))
    delete_movie_button.grid(row=len(movie_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_movies_button = ttk.Button(movies_tab, text="Display All Movies", command=lambda: display_all_movies(movies_tree))
    display_all_movies_button.grid(row=len(movie_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    for col in movie_columns:
        movies_tree.heading(col, text=col)
        movies_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    movies_tree.grid(row=len(movie_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    movies_scroll = ttk.Scrollbar(movies_tab, orient='vertical', command=movies_tree.yview)
    movies_scroll.grid(row=len(movie_labels) + 3, column=2, sticky='ns')
    movies_tree.configure(yscroll=movies_scroll.set)

    movies_hscroll = ttk.Scrollbar(movies_tab, orient='horizontal', command=movies_tree.xview)
    movies_hscroll.grid(row=len(movie_labels) + 4, column=0, columnspan=2, sticky='ew')
    movies_tree.configure(xscroll=movies_hscroll.set)

    return movies_tab

def create_screens_tab(notebook):
    screens_tab = ttk.Frame(notebook)
    notebook.add(screens_tab, text='Screens')

    # Entry fields for screen data
    screen_labels = ["TheaterID", "ScreenName", "SeatCapacity"]
    screen_entries = []
    # Treeview for Screens
    screen_columns = ("ScreenID", "TheaterID", "ScreenName", "SeatCapacity")
    screens_tree = ttk.Treeview(screens_tab, columns=screen_columns, show='headings', height=8)

    for i, label in enumerate(screen_labels):
        lbl = ttk.Label(screens_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(screens_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        screen_entries.append(entry)

    # ScreenID field for update and delete operations
    screen_id_label = ttk.Label(screens_tab, text="ScreenID")
    screen_id_label.grid(row=len(screen_labels), column=0, padx=10, pady=10, sticky='W')
    screen_id_entry = ttk.Entry(screens_tab)
    screen_id_entry.grid(row=len(screen_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_screen_button = ttk.Button(screens_tab, text="Insert Screen", command=lambda: insert_screen(screen_entries,screens_tree))
    insert_screen_button.grid(row=len(screen_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_screen_button = ttk.Button(screens_tab, text="Update Screen", command=lambda: update_screen(screen_entries, screen_id_entry.get(),screens_tree))
    update_screen_button.grid(row=len(screen_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_screen_button = ttk.Button(screens_tab, text="Delete Screen", command=lambda: delete_screen(screen_id_entry.get(),screens_tree))
    delete_screen_button.grid(row=len(screen_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_screens_button = ttk.Button(screens_tab, text="Display All Screens", command=lambda: display_all_screens(screens_tree))
    display_all_screens_button.grid(row=len(screen_labels) + 2, column=1, padx=10, pady=10, sticky='W')


    for col in screen_columns:
        screens_tree.heading(col, text=col)
        screens_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    screens_tree.grid(row=len(screen_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    screens_scroll = ttk.Scrollbar(screens_tab, orient='vertical', command=screens_tree.yview)
    screens_scroll.grid(row=len(screen_labels) + 3, column=2, sticky='ns')
    screens_tree.configure(yscroll=screens_scroll.set)

    screens_hscroll = ttk.Scrollbar(screens_tab, orient='horizontal', command=screens_tree.xview)
    screens_hscroll.grid(row=len(screen_labels) + 4, column=0, columnspan=2, sticky='ew')
    screens_tree.configure(xscroll=screens_hscroll.set)

    # Populate the Treeview with data
    display_all_screens(screens_tree)

    return screens_tab

def create_showtimes_tab(notebook):
    showtimes_tab = ttk.Frame(notebook)
    notebook.add(showtimes_tab, text='Showtimes')

    # Entry fields for showtime data
    showtime_labels = ["MovieID", "TheaterID", "ScreenID", "StartTime", "EndTime", "Date", "TicketPrice"]
    showtime_entries = []

    for i, label in enumerate(showtime_labels):
        lbl = ttk.Label(showtimes_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(showtimes_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        showtime_entries.append(entry)

    # ShowtimeID field for update and delete operations
    showtime_id_label = ttk.Label(showtimes_tab, text="ShowtimeID")
    showtime_id_label.grid(row=len(showtime_labels), column=0, padx=10, pady=10, sticky='W')
    showtime_id_entry = ttk.Entry(showtimes_tab)
    showtime_id_entry.grid(row=len(showtime_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_showtime_button = ttk.Button(showtimes_tab, text="Insert Showtime", command=lambda: insert_showtime(showtime_entries, showtimes_tree))
    insert_showtime_button.grid(row=len(showtime_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_showtime_button = ttk.Button(showtimes_tab, text="Update Showtime", command=lambda: update_showtime(showtime_entries, showtime_id_entry.get(), showtimes_tree))
    update_showtime_button.grid(row=len(showtime_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_showtime_button = ttk.Button(showtimes_tab, text="Delete Showtime", command=lambda: delete_showtime(showtime_id_entry.get(), showtimes_tree))
    delete_showtime_button.grid(row=len(showtime_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_showtimes_button = ttk.Button(showtimes_tab, text="Display All Showtimes", command=lambda: display_all_showtimes(showtimes_tree))
    display_all_showtimes_button.grid(row=len(showtime_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for Showtimes
    showtime_columns = ("ShowtimeID", "MovieID", "TheaterID", "ScreenID", "StartTime", "EndTime", "Date", "TicketPrice")
    showtimes_tree = ttk.Treeview(showtimes_tab, columns=showtime_columns, show='headings', height=8)

    for col in showtime_columns:
        showtimes_tree.heading(col, text=col)
        showtimes_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    showtimes_tree.grid(row=len(showtime_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    showtimes_scroll = ttk.Scrollbar(showtimes_tab, orient='vertical', command=showtimes_tree.yview)
    showtimes_scroll.grid(row=len(showtime_labels) + 3, column=2, sticky='ns')
    showtimes_tree.configure(yscroll=showtimes_scroll.set)

    showtimes_hscroll = ttk.Scrollbar(showtimes_tab, orient='horizontal', command=showtimes_tree.xview)
    showtimes_hscroll.grid(row=len(showtime_labels) + 4, column=0, columnspan=2, sticky='ew')
    showtimes_tree.configure(xscroll=showtimes_hscroll.set)

    # Populate the Treeview with data
    display_all_showtimes(showtimes_tree)

    return showtimes_tab

def create_tickets_tab(notebook):
    tickets_tab = ttk.Frame(notebook)
    notebook.add(tickets_tab, text='Tickets')

    # Entry fields for ticket data
    ticket_labels = ["ShowtimeID", "UserID", "BookingTime", "TotalAmount", "SeatNumber"]
    ticket_entries = []

    for i, label in enumerate(ticket_labels):
        lbl = ttk.Label(tickets_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(tickets_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        ticket_entries.append(entry)

    # TicketID field for update and delete operations
    ticket_id_label = ttk.Label(tickets_tab, text="TicketID")
    ticket_id_label.grid(row=len(ticket_labels), column=0, padx=10, pady=10, sticky='W')
    ticket_id_entry = ttk.Entry(tickets_tab)
    ticket_id_entry.grid(row=len(ticket_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_ticket_button = ttk.Button(tickets_tab, text="Insert Ticket", command=lambda: insert_ticket(ticket_entries, tickets_tree))
    insert_ticket_button.grid(row=len(ticket_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_ticket_button = ttk.Button(tickets_tab, text="Update Ticket", command=lambda: update_ticket(ticket_entries, ticket_id_entry.get(), tickets_tree))
    update_ticket_button.grid(row=len(ticket_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_ticket_button = ttk.Button(tickets_tab, text="Delete Ticket", command=lambda: delete_ticket(ticket_id_entry.get(), tickets_tree))
    delete_ticket_button.grid(row=len(ticket_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_tickets_button = ttk.Button(tickets_tab, text="Display All Tickets", command=lambda: display_all_tickets(tickets_tree))
    display_all_tickets_button.grid(row=len(ticket_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for Tickets
    ticket_columns = ("TicketID", "ShowtimeID", "UserID", "BookingTime", "TotalAmount", "SeatNumber")
    tickets_tree = ttk.Treeview(tickets_tab, columns=ticket_columns, show='headings', height=8)

    for col in ticket_columns:
        tickets_tree.heading(col, text=col)
        tickets_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    tickets_tree.grid(row=len(ticket_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    tickets_scroll = ttk.Scrollbar(tickets_tab, orient='vertical', command=tickets_tree.yview)
    tickets_scroll.grid(row=len(ticket_labels) + 3, column=2, sticky='ns')
    tickets_tree.configure(yscroll=tickets_scroll.set)

    tickets_hscroll = ttk.Scrollbar(tickets_tab, orient='horizontal', command=tickets_tree.xview)
    tickets_hscroll.grid(row=len(ticket_labels) + 4, column=0, columnspan=2, sticky='ew')
    tickets_tree.configure(xscroll=tickets_hscroll.set)

    # Populate the Treeview with data
    display_all_tickets(tickets_tree)

    return tickets_tab

def create_payments_tab(notebook):
    payments_tab = ttk.Frame(notebook)
    notebook.add(payments_tab, text='Payments')

    # Entry fields for payment data
    payment_labels = ["TicketID", "PaymentMethod", "Amount", "PaymentStatus", "TransactionID"]
    payment_entries = []

    for i, label in enumerate(payment_labels):
        lbl = ttk.Label(payments_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(payments_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        payment_entries.append(entry)

    # PaymentID field for update and delete operations
    payment_id_label = ttk.Label(payments_tab, text="PaymentID")
    payment_id_label.grid(row=len(payment_labels), column=0, padx=10, pady=10, sticky='W')
    payment_id_entry = ttk.Entry(payments_tab)
    payment_id_entry.grid(row=len(payment_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_payment_button = ttk.Button(payments_tab, text="Insert Payment", command=lambda: insert_payment(payment_entries, payments_tree))
    insert_payment_button.grid(row=len(payment_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_payment_button = ttk.Button(payments_tab, text="Update Payment", command=lambda: update_payment(payment_entries, payment_id_entry.get(), payments_tree))
    update_payment_button.grid(row=len(payment_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_payment_button = ttk.Button(payments_tab, text="Delete Payment", command=lambda: delete_payment(payment_id_entry.get(), payments_tree))
    delete_payment_button.grid(row=len(payment_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_payments_button = ttk.Button(payments_tab, text="Display All Payments", command=lambda: display_all_payments(payments_tree))
    display_all_payments_button.grid(row=len(payment_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for Payments
    payment_columns = ("PaymentID", "TicketID", "PaymentMethod", "Amount", "PaymentStatus", "TransactionID")
    payments_tree = ttk.Treeview(payments_tab, columns=payment_columns, show='headings', height=8)

    for col in payment_columns:
        payments_tree.heading(col, text=col)
        payments_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    payments_tree.grid(row=len(payment_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    payments_scroll = ttk.Scrollbar(payments_tab, orient='vertical', command=payments_tree.yview)
    payments_scroll.grid(row=len(payment_labels) + 3, column=2, sticky='ns')
    payments_tree.configure(yscroll=payments_scroll.set)

    payments_hscroll = ttk.Scrollbar(payments_tab, orient='horizontal', command=payments_tree.xview)
    payments_hscroll.grid(row=len(payment_labels) + 4, column=0, columnspan=2, sticky='ew')
    payments_tree.configure(xscroll=payments_hscroll.set)

    # Populate the Treeview with data
    display_all_payments(payments_tree)

    return payments_tab

def create_promotions_tab(notebook):
    promotions_tab = ttk.Frame(notebook)
    notebook.add(promotions_tab, text='Promotions')

    # Entry fields for promotion data
    promotion_labels = ["Code", "Description", "DiscountPercentage", "ValidFrom", "ValidTill"]
    promotion_entries = []

    for i, label in enumerate(promotion_labels):
        lbl = ttk.Label(promotions_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(promotions_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        promotion_entries.append(entry)

    # PromoID field for update and delete operations
    promo_id_label = ttk.Label(promotions_tab, text="PromoID")
    promo_id_label.grid(row=len(promotion_labels), column=0, padx=10, pady=10, sticky='W')
    promo_id_entry = ttk.Entry(promotions_tab)
    promo_id_entry.grid(row=len(promotion_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_promotion_button = ttk.Button(promotions_tab, text="Insert Promotion", command=lambda: insert_promotion(promotion_entries, promotions_tree))
    insert_promotion_button.grid(row=len(promotion_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_promotion_button = ttk.Button(promotions_tab, text="Update Promotion", command=lambda: update_promotion(promotion_entries, promo_id_entry.get(), promotions_tree))
    update_promotion_button.grid(row=len(promotion_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_promotion_button = ttk.Button(promotions_tab, text="Delete Promotion", command=lambda: delete_promotion(promo_id_entry.get(), promotions_tree))
    delete_promotion_button.grid(row=len(promotion_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_promotions_button = ttk.Button(promotions_tab, text="Display All Promotions", command=lambda: display_all_promotions(promotions_tree))
    display_all_promotions_button.grid(row=len(promotion_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for Promotions
    promotion_columns = ("PromoID", "Code", "Description", "DiscountPercentage", "ValidFrom", "ValidTill")
    promotions_tree = ttk.Treeview(promotions_tab, columns=promotion_columns, show='headings', height=8)

    for col in promotion_columns:
        promotions_tree.heading(col, text=col)
        promotions_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    promotions_tree.grid(row=len(promotion_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    promotions_scroll = ttk.Scrollbar(promotions_tab, orient='vertical', command=promotions_tree.yview)
    promotions_scroll.grid(row=len(promotion_labels) + 3, column=2, sticky='ns')
    promotions_tree.configure(yscroll=promotions_scroll.set)

    promotions_hscroll = ttk.Scrollbar(promotions_tab, orient='horizontal', command=promotions_tree.xview)
    promotions_hscroll.grid(row=len(promotion_labels) + 4, column=0, columnspan=2, sticky='ew')
    promotions_tree.configure(xscroll=promotions_hscroll.set)

    # Populate the Treeview with data
    display_all_promotions(promotions_tree)

    return promotions_tab

def create_user_promotions_tab(notebook):
    user_promotions_tab = ttk.Frame(notebook)
    notebook.add(user_promotions_tab, text='User Promotions')

    # Entry fields for user promotion data
    user_promotion_labels = ["UserID", "PromoID", "DateUsed"]
    user_promotion_entries = []

    for i, label in enumerate(user_promotion_labels):
        lbl = ttk.Label(user_promotions_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        entry = ttk.Entry(user_promotions_tab)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        user_promotion_entries.append(entry)

    # UserPromoID field for update and delete operations
    user_promo_id_label = ttk.Label(user_promotions_tab, text="UserPromoID")
    user_promo_id_label.grid(row=len(user_promotion_labels), column=0, padx=10, pady=10, sticky='W')
    user_promo_id_entry = ttk.Entry(user_promotions_tab)
    user_promo_id_entry.grid(row=len(user_promotion_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_user_promotion_button = ttk.Button(user_promotions_tab, text="Insert User Promotion", command=lambda: insert_user_promotion(user_promotion_entries, user_promotions_tree))
    insert_user_promotion_button.grid(row=len(user_promotion_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_user_promotion_button = ttk.Button(user_promotions_tab, text="Update User Promotion", command=lambda: update_user_promotion(user_promotion_entries, user_promo_id_entry.get(), user_promotions_tree))
    update_user_promotion_button.grid(row=len(user_promotion_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_user_promotion_button = ttk.Button(user_promotions_tab, text="Delete User Promotion", command=lambda: delete_user_promotion(user_promo_id_entry.get(), user_promotions_tree))
    delete_user_promotion_button.grid(row=len(user_promotion_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_user_promotions_button = ttk.Button(user_promotions_tab, text="Display All User Promotions", command=lambda: display_all_user_promotions(user_promotions_tree))
    display_all_user_promotions_button.grid(row=len(user_promotion_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for UserPromotions
    user_promotion_columns = ("UserPromoID", "UserID", "PromoID", "DateUsed")
    user_promotions_tree = ttk.Treeview(user_promotions_tab, columns=user_promotion_columns, show='headings', height=8)

    for col in user_promotion_columns:
        user_promotions_tree.heading(col, text=col)
        user_promotions_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    user_promotions_tree.grid(row=len(user_promotion_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    user_promotions_scroll = ttk.Scrollbar(user_promotions_tab, orient='vertical', command=user_promotions_tree.yview)
    user_promotions_scroll.grid(row=len(user_promotion_labels) + 3, column=2, sticky='ns')
    user_promotions_tree.configure(yscroll=user_promotions_scroll.set)

    user_promotions_hscroll = ttk.Scrollbar(user_promotions_tab, orient='horizontal', command=user_promotions_tree.xview)
    user_promotions_hscroll.grid(row=len(user_promotion_labels) + 4, column=0, columnspan=2, sticky='ew')
    user_promotions_tree.configure(xscroll=user_promotions_hscroll.set)

    # Populate the Treeview with data
    display_all_user_promotions(user_promotions_tree)

    return user_promotions_tab

def create_ratings_reviews_tab(notebook):
    ratings_reviews_tab = ttk.Frame(notebook)
    notebook.add(ratings_reviews_tab, text='Ratings & Reviews')

    # Entry fields for rating and review data
    rating_review_labels = ["UserID", "MovieID", "Rating", "Review"]
    rating_review_entries = []

    for i, label in enumerate(rating_review_labels):
        lbl = ttk.Label(ratings_reviews_tab, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10, sticky='W')
        if label == "Review":  # Use a Text widget for multi-line input
            entry = tk.Text(ratings_reviews_tab, height=4, width=50)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        else:
            entry = ttk.Entry(ratings_reviews_tab)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky='EW')
        rating_review_entries.append(entry)

    # RatingReviewID field for update and delete operations
    rating_review_id_label = ttk.Label(ratings_reviews_tab, text="RatingReviewID")
    rating_review_id_label.grid(row=len(rating_review_labels), column=0, padx=10, pady=10, sticky='W')
    rating_review_id_entry = ttk.Entry(ratings_reviews_tab)
    rating_review_id_entry.grid(row=len(rating_review_labels), column=1, padx=10, pady=10, sticky='EW')

    # Buttons for CRUD operations
    insert_rating_review_button = ttk.Button(ratings_reviews_tab, text="Insert Rating/Review", command=lambda: insert_rating_review(rating_review_entries, ratings_reviews_tree))
    insert_rating_review_button.grid(row=len(rating_review_labels) + 1, column=0, padx=10, pady=10, sticky='W')

    update_rating_review_button = ttk.Button(ratings_reviews_tab, text="Update Rating/Review", command=lambda: update_rating_review(rating_review_entries, rating_review_id_entry.get(), ratings_reviews_tree))
    update_rating_review_button.grid(row=len(rating_review_labels) + 1, column=1, padx=10, pady=10, sticky='W')

    delete_rating_review_button = ttk.Button(ratings_reviews_tab, text="Delete Rating/Review", command=lambda: delete_rating_review(rating_review_id_entry.get(), ratings_reviews_tree))
    delete_rating_review_button.grid(row=len(rating_review_labels) + 2, column=0, padx=10, pady=10, sticky='W')

    display_all_ratings_reviews_button = ttk.Button(ratings_reviews_tab, text="Display All Ratings/Reviews", command=lambda: display_all_ratings_reviews(ratings_reviews_tree))
    display_all_ratings_reviews_button.grid(row=len(rating_review_labels) + 2, column=1, padx=10, pady=10, sticky='W')

    # Treeview for RatingsReviews
    rating_review_columns = ("RatingReviewID", "UserID", "MovieID", "Rating", "Review")
    ratings_reviews_tree = ttk.Treeview(ratings_reviews_tab, columns=rating_review_columns, show='headings', height=8)

    for col in rating_review_columns:
        ratings_reviews_tree.heading(col, text=col)
        ratings_reviews_tree.column(col, anchor='w', width=100)  # Adjust the width as necessary

    ratings_reviews_tree.grid(row=len(rating_review_labels) + 3, column=0, columnspan=2, padx=10, pady=10, sticky='EWNS')

    # Scrollbars for the Treeview
    ratings_reviews_scroll = ttk.Scrollbar(ratings_reviews_tab, orient='vertical', command=ratings_reviews_tree.yview)
    ratings_reviews_scroll.grid(row=len(rating_review_labels) + 3, column=2, sticky='ns')
    ratings_reviews_tree.configure(yscroll=ratings_reviews_scroll.set)

    ratings_reviews_hscroll = ttk.Scrollbar(ratings_reviews_tab, orient='horizontal', command=ratings_reviews_tree.xview)
    ratings_reviews_hscroll.grid(row=len(rating_review_labels) + 4, column=0, columnspan=2, sticky='ew')
    ratings_reviews_tree.configure(xscroll=ratings_reviews_hscroll.set)

    # Populate the Treeview with data
    display_all_ratings_reviews(ratings_reviews_tree)

    return ratings_reviews_tab


# Initialize the main window
root = tk.Tk()
root.title("Movie Ticketing System Database Interface")
root.withdraw()
# Create the Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')  # Expand the notebook to fill the window

# Create a tab for each entity
users_tab = create_users_tab(notebook)
theaters_tab = create_theaters_tab(notebook)
movies_tab = create_movies_tab(notebook)
screens_tab = create_screens_tab(notebook)
showtimes_tab = create_showtimes_tab(notebook)
tickets_tab = create_tickets_tab(notebook)
payments_tab = create_payments_tab(notebook)
promotions_tab = create_promotions_tab(notebook)
user_promotions_tab = create_user_promotions_tab(notebook)
ratings_reviews_tab = create_ratings_reviews_tab(notebook)

# Add tabs to the notebook
notebook.add(users_tab, text='Users')
notebook.add(theaters_tab, text='Theaters')
notebook.add(movies_tab, text='Movies')
notebook.add(screens_tab, text='Screens')
notebook.add(showtimes_tab, text='Showtimes')
notebook.add(tickets_tab, text='Tickets')
notebook.add(payments_tab, text='Payments')
notebook.add(promotions_tab, text='Promotions')
notebook.add(user_promotions_tab, text='User Promotions')
notebook.add(ratings_reviews_tab, text='Ratings & Reviews')

if args.nologin:
    root.deiconify()
else:
    login_win = create_login_window()

# Start the main loop
root.mainloop()
