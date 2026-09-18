import uuid
from database.database import get_connection
from services import data_store
from models.booking import Booking
from services.flight_service import FlightService

class ReservationService:
    @staticmethod
    def save_passenger_details(booking_ref, info, conn=None):
        """Stores passenger contact details against a booking or waitlist reference.
        Pass conn to join an existing transaction instead of opening a new one."""
        own = conn is None
        if own:
            conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO passenger_details
            (booking_ref, full_name, age, gender, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_ref,
            info.get('full_name', '').strip(),
            info.get('age'),
            info.get('gender', ''),
            info.get('phone', '').strip(),
            info.get('email', '').strip(),
            info.get('address', '').strip(),
        ))
        if own:
            conn.commit()
            conn.close()

    @staticmethod
    def get_passenger_details(booking_ref, conn=None):
        """Returns passenger details for a booking/waitlist reference, or None."""
        own = conn is None
        if own:
            conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, age, gender, phone, email, address FROM passenger_details WHERE booking_ref = ?',
                       (booking_ref,))
        row = cursor.fetchone()
        if own:
            conn.close()
        if not row:
            return None
        return {'full_name': row[0], 'age': row[1], 'gender': row[2], 'phone': row[3], 'email': row[4], 'address': row[5]}

    @staticmethod
    def book_ticket(user_id, flight_number, passenger_info=None):
        """Books a ticket, updates seats, or adds to Waiting List Priority Queue.
        If passenger_info (dict) is provided, it is persisted against the booking."""
        # 1. Find flight in AVL Tree
        flight = FlightService.search_flight(flight_number)
        if not flight:
            return False, "Flight not found."
        
        # 2. Check if flight is full
        if flight.available_seats <= 0:
            # Add to priority queue (Waiting List)
            priority = len(data_store.waiting_list_pq.heap) + 1 # First come, first serve priority
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO waiting_list (user_id, flight_number, priority) VALUES (?, ?, ?)', 
                           (user_id, flight_number, priority))
            conn.commit()
            
            # Get the generated ID
            cursor.execute('SELECT last_insert_rowid()')
            wait_id = cursor.fetchone()[0]
            conn.close()
            
            # Insert into our Priority Queue structure
            data_store.waiting_list_pq.insert({'wait_id': wait_id, 'user_id': user_id, 'flight_number': flight_number}, priority)

            # Keep the passenger's details attached to their waitlist entry so they
            # travel with the booking when the Min-Heap promotes them.
            if passenger_info:
                ReservationService.save_passenger_details(f'W{wait_id}', passenger_info)

            return False, "Flight is full. You have been added to the Priority Waiting List."

        # 3. Generate Booking ID and update Seats
        # Using uuid to create a unique 8-character ID
        booking_id = "BKG-" + str(uuid.uuid4())[:8].upper()
        flight.available_seats -= 1

        # 4. Save to SQLite
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookings (booking_id, user_id, flight_number, status) VALUES (?, ?, ?, ?)',
                       (booking_id, user_id, flight_number, 'CONFIRMED'))
        cursor.execute('UPDATE flights SET available_seats = ? WHERE flight_number = ?', 
                       (flight.available_seats, flight_number))
        conn.commit()
        conn.close()

        # 5. Save to Booking AVL Tree
        b = Booking(booking_id, user_id, flight_number, 'CONFIRMED', 'Just Now')
        data_store.booking_root = data_store.booking_tree.insert(data_store.booking_root, booking_id, b)

        # 6. Save passenger details captured from the booking form
        if passenger_info:
            ReservationService.save_passenger_details(booking_id, passenger_info)

        return True, f"Ticket booked successfully!\nYour Booking ID is: {booking_id}"