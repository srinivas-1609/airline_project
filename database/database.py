import sqlite3
import datetime

def get_connection():
    return sqlite3.connect('airline.db')

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS flights (flight_number TEXT PRIMARY KEY, airline TEXT, source TEXT, destination TEXT, flight_date TEXT, dep_time TEXT, arr_time TEXT, total_seats INTEGER, available_seats INTEGER, price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (booking_id TEXT PRIMARY KEY, user_id INTEGER, flight_number TEXT, status TEXT, booking_date TEXT, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(flight_number) REFERENCES flights(flight_number))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS waiting_list (wait_id TEXT PRIMARY KEY, user_id INTEGER, flight_number TEXT, priority TEXT, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(flight_number) REFERENCES flights(flight_number))''')
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role, name) VALUES ('admin', 'admin123', 'admin', 'System Admin')")
        cursor.execute("INSERT INTO users (username, password, role, name) VALUES ('johndoe', 'pass123', 'passenger', 'John Doe')")
    
    cursor.execute("SELECT COUNT(*) FROM flights")
    if cursor.fetchone()[0] == 0:
        today = datetime.date.today().isoformat()
        flights = [
            ('IG101', 'IndiGo', 'DEL', 'BOM', today, '06:00', '08:10', 180, 180, 4500.0),
            ('AI102', 'Air India', 'DEL', 'BLR', today, '07:30', '10:15', 200, 200, 5500.0),
            ('SJ103', 'SpiceJet', 'DEL', 'HYD', today, '08:00', '10:15', 150, 150, 4200.0),
            ('UK104', 'Vistara', 'DEL', 'MAA', today, '09:00', '11:45', 160, 160, 5800.0),
            ('AK105', 'Akasa Air', 'DEL', 'CCU', today, '10:15', '12:30', 180, 180, 4800.0),
            ('IG106', 'IndiGo', 'DEL', 'SXR', today, '11:30', '13:00', 180, 180, 3500.0),
            ('AI107', 'Air India', 'DEL', 'JAI', today, '12:45', '13:45', 120, 120, 2500.0),
            ('SJ108', 'SpiceJet', 'DEL', 'LKO', today, '14:00', '15:10', 150, 150, 2800.0),
            ('UK109', 'Vistara', 'DEL', 'ATQ', today, '15:30', '16:40', 160, 160, 2600.0),
            ('AK110', 'Akasa Air', 'BOM', 'GOI', today, '06:30', '07:45', 180, 180, 3000.0),
            ('IG111', 'IndiGo', 'BOM', 'PNQ', today, '08:00', '08:45', 120, 120, 1500.0),
            ('AI112', 'Air India', 'BOM', 'BLR', today, '09:30', '11:15', 200, 200, 3500.0),
            ('SJ113', 'SpiceJet', 'BOM', 'AMD', today, '11:00', '12:15', 150, 150, 3200.0),
            ('UK114', 'Vistara', 'BLR', 'MAA', today, '07:00', '08:00', 160, 160, 2500.0),
            ('AK115', 'Akasa Air', 'BLR', 'TRV', today, '08:30', '10:00', 180, 180, 3800.0),
            ('IG116', 'IndiGo', 'BLR', 'COK', today, '10:15', '11:30', 180, 180, 3600.0),
            ('AI117', 'Air India', 'HYD', 'BLR', today, '12:00', '13:10', 200, 200, 3000.0),
            ('SJ118', 'SpiceJet', 'HYD', 'MAA', today, '14:30', '15:45', 150, 150, 3200.0),
            ('UK119', 'Vistara', 'HYD', 'PNQ', today, '16:00', '17:15', 160, 160, 3400.0),
            ('AK120', 'Akasa Air', 'CCU', 'MAA', today, '17:30', '19:45', 180, 180, 4500.0),
            ('IG121', 'IndiGo', 'AMD', 'JAI', today, '19:00', '20:15', 180, 180, 3000.0),
            ('AI122', 'Air India', 'TRV', 'COK', today, '21:30', '22:15', 120, 120, 1800.0),
            ('SJ123', 'SpiceJet', 'AMD', 'BLR', today, '06:15', '08:30', 150, 150, 4300.0),
            ('UK124', 'Vistara', 'TRV', 'DEL', today, '08:45', '12:15', 160, 160, 7500.0),
            ('IG201', 'IndiGo', 'BOM', 'DEL', today, '10:00', '12:10', 180, 180, 4600.0),
            ('AI202', 'Air India', 'BLR', 'DEL', today, '13:00', '15:45', 200, 200, 5600.0),
            ('SJ203', 'SpiceJet', 'HYD', 'DEL', today, '16:00', '18:15', 150, 150, 4300.0),
            ('UK204', 'Vistara', 'MAA', 'DEL', today, '19:00', '21:45', 160, 160, 5900.0),
            ('AK205', 'Akasa Air', 'CCU', 'DEL', today, '22:15', '00:30', 180, 180, 4900.0),
            ('IG206', 'IndiGo', 'SXR', 'DEL', today, '08:30', '10:00', 180, 180, 3600.0),
            ('AI207', 'Air India', 'JAI', 'DEL', today, '15:45', '16:45', 120, 120, 2600.0),
            ('SJ208', 'SpiceJet', 'LKO', 'DEL', today, '18:00', '19:10', 150, 150, 2900.0),
            ('UK209', 'Vistara', 'ATQ', 'DEL', today, '20:30', '21:40', 160, 160, 2700.0),
            ('AK210', 'Akasa Air', 'GOI', 'BOM', today, '09:30', '10:45', 180, 180, 3100.0),
            ('IG211', 'IndiGo', 'PNQ', 'BOM', today, '11:00', '11:45', 120, 120, 1600.0),
            ('AI212', 'Air India', 'BLR', 'BOM', today, '13:30', '15:15', 200, 200, 3600.0),
            ('SJ213', 'SpiceJet', 'AMD', 'BOM', today, '16:00', '17:15', 150, 150, 3300.0),
            ('UK214', 'Vistara', 'MAA', 'BLR', today, '10:00', '11:00', 160, 160, 2600.0),
            ('AK215', 'Akasa Air', 'TRV', 'BLR', today, '12:30', '14:00', 180, 180, 3900.0),
            ('IG216', 'IndiGo', 'COK', 'BLR', today, '15:15', '16:30', 180, 180, 3700.0)
        ]
        cursor.executemany("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)
        
    conn.commit()
    conn.close()