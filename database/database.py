import sqlite3
import os

DB_NAME = 'airline_reservation_system/database/airline.db'

def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    return sqlite3.connect(DB_NAME)

def setup_database():
    """Creates the necessary tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table (Used for Hash Table integration later)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL -- 'admin' or 'passenger'
        )
    ''')

    # 2. Airports Table (Graph Nodes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    # 3. Routes Table (Graph Edges / Dijkstra)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            route_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            distance INTEGER NOT NULL,
            FOREIGN KEY (source) REFERENCES airports(code),
            FOREIGN KEY (destination) REFERENCES airports(code)
        )
    ''')

    # 4. Flights Table (Flight Number AVL Tree)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            flight_number TEXT PRIMARY KEY,
            airline TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            flight_date TEXT NOT NULL,
            dep_time TEXT NOT NULL,
            arr_time TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (source) REFERENCES airports(code),
            FOREIGN KEY (destination) REFERENCES airports(code)
        )
    ''')

    # 5. Bookings Table (Booking ID AVL Tree)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            flight_number TEXT NOT NULL,
            status TEXT NOT NULL, -- 'CONFIRMED' or 'CANCELLED'
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
        )
    ''')

    # 6. Waiting List Table (Priority Queue)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS waiting_list (
            wait_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            flight_number TEXT NOT NULL,
            priority INTEGER NOT NULL,
            request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
        )
    ''')

    conn.commit()
    conn.close()

def insert_sample_data():
    """Inserts dummy data for initial testing and demonstration."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if data already exists to prevent duplicate insertion errors
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Data already seeded

    # Insert Admin and Passenger
    # Note: In a real app, passwords should be hashed. We will handle hashing logic in the Service layer later.
    cursor.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES ('admin', 'admin123', 'System Admin', 'admin@airline.com', '0000000000', 'admin')")
    cursor.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES ('johndoe', 'pass123', 'John Doe', 'john@example.com', '1234567890', 'passenger')")

    # Insert Airports
    airports = [
        ('HYD', 'Rajiv Gandhi Intl', 'Hyderabad'),
        ('DEL', 'Indira Gandhi Intl', 'Delhi'),
        ('BOM', 'Chhatrapati Shivaji', 'Mumbai'),
        ('BLR', 'Kempegowda Intl', 'Bangalore'),
        ('MAA', 'Chennai Intl', 'Chennai')
    ]
    cursor.executemany("INSERT INTO airports (code, name, city) VALUES (?, ?, ?)", airports)

    # Insert Routes (for Dijkstra)
    routes = [
        ('HYD', 'BLR', 500),
        ('HYD', 'BOM', 700),
        ('BOM', 'DEL', 1150),
        ('BLR', 'DEL', 1700),
        ('HYD', 'DEL', 1500),
        ('BOM', 'MAA', 1030),
        ('BLR', 'MAA', 350)
    ]
    for src, dest, dist in routes:
        cursor.execute("INSERT INTO routes (source, destination, distance) VALUES (?, ?, ?)", (src, dest, dist))
        # Assuming undirected graph for flights (two-way routes)
        cursor.execute("INSERT INTO routes (source, destination, distance) VALUES (?, ?, ?)", (dest, src, dist))

    # Insert Flights
    flights = [
        ('FL101', 'Air India', 'HYD', 'DEL', '2023-12-01', '08:00', '10:30', 100, 100, 5500.00),
        ('FL102', 'IndiGo', 'BOM', 'DEL', '2023-12-01', '09:00', '11:15', 150, 150, 4200.00),
        ('FL103', 'SpiceJet', 'HYD', 'BLR', '2023-12-01', '06:30', '07:45', 50, 50, 2500.00)
    ]
    cursor.executemany("INSERT INTO flights (flight_number, airline, source, destination, flight_date, dep_time, arr_time, total_seats, available_seats, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    insert_sample_data()
    print("Database setup complete and sample data inserted successfully.")