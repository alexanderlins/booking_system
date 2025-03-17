import sqlite3
import bcrypt
from pathlib import Path

# A function for creating a hashed password
def hash_password(plain_password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode(), salt)

## INITIAL SETUP
def initial_setup():
    # Inserting a dummy user into the SQLITE database
    my_file = Path("bookingsystem.db")
    if my_file.is_file():
        print("Database exists")
    else:
        with open('bookingsystem.db', 'w') as file:
            print("Creating database...")
        
        customer_name = "admin"
        customer_password = "admin"
        hashed_password = hash_password(customer_password)

        # Connect to (or create) a database
        conn = sqlite3.connect("bookingsystem.db")

        # Create a cursor object for accessing database
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(25) NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE NOT NULL CHECK (LENGTH(name) >= 3),
                password TEXT NOT NULL  
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER UNIQUE REFERENCES customer(customer_id) ON DELETE CASCADE,
                room_id INTEGER UNIQUE REFERENCES room(room_id) ON DELETE CASCADE,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                CONSTRAINT check_dates CHECK (check_out_date > check_in_date)
            )
        ''')

        # Add dummy user with hashed password
        cursor.execute("INSERT INTO customer (name, password) VALUES (?, ?)", (customer_name, hashed_password))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

def create_new_user(name: str, password: str) -> bool:
    encrypted_password = hash_password(password)
    conn = sqlite3.connect("bookingsystem.db")
    cursor = conn.cursor()
        
    # Insert the new user
    try:
        cursor.execute("INSERT INTO customer (name, password) VALUES (?, ?)", (name, encrypted_password))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("This username is already taken. Please choose a different one.")
        elif "CHECK constraint failed" in str(e):
            print("User not created. Make sure to write more than 3 characters.")
        return False
        
    # Query to check if the user was added
    cursor.execute("SELECT name FROM customer WHERE name = ?", (name,))
    result = cursor.fetchone()  # Call the method
    
    conn.close()
    
    # Check if a result was returned and that the name matches
    if result is not None and result[0] == name:
        print("User added")
        return True
    else:
        return False

def login(name: str, password: str) -> bool:
    with sqlite3.connect("bookingsystem.db") as conn:
        cursor = conn.cursor()
        # Retrieve the stored hashed password for the given username
        cursor.execute('SELECT customer_id, password FROM customer WHERE name = ?', (name,))
        result = cursor.fetchone()
        
        if result:
            customer_id, stored_hash = result
            # Encode the provided password to bytes
            password_bytes = password.encode('utf-8')
            # Encode the stored hash to bytes (if it's not already in byte format)
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            # Verify the provided password against the stored hash
            if bcrypt.checkpw(password_bytes, stored_hash):
                print(f"Login successful. Customer ID: {customer_id}, Name: {name}")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Username not found.")
            return False
