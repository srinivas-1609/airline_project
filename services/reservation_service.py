import uuid
from database.database import get_connection
from services import data_store
from models.booking import Booking
from services.flight_service import FlightService

class ReservationService:
    @staticmethod
    def book_ticket(user_id, flight_number):
        """Books a ticket, updates seats, or adds to Waiting List Priority Queue."""
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

        return True, f"Ticket booked successfully!\nYour Booking ID is: {booking_id}"