import uuid
import datetime
from database.database import get_connection
from services import data_store
from models.booking import Booking

class ReservationService:
    @staticmethod
    def book_ticket(user_id, flight_number, passenger_info=None):
        """Books a ticket in O(log n) time using the AVL Tree."""
        
        # 1. Search for the flight in O(log n) time
        flight_node = data_store.flight_tree.search(data_store.flight_root, flight_number)
        if not flight_node:
            return False, "Flight not found."
            
        flight = flight_node.data
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # 2. Check if seats are available
            if flight.available_seats > 0:
                # Generate unique booking ID
                booking_id = f"BKG-{uuid.uuid4().hex[:8].upper()}"
                date_now = datetime.datetime.now().isoformat()
                
                # Insert into SQLite Database
                cursor.execute(
                    'INSERT INTO bookings (booking_id, user_id, flight_number, status, booking_date) VALUES (?, ?, ?, ?, ?)',
                    (booking_id, user_id, flight_number, 'CONFIRMED', date_now)
                )
                
                # Deduct 1 seat and update database
                flight.available_seats -= 1
                cursor.execute('UPDATE flights SET available_seats = ? WHERE flight_number = ?', 
                             (flight.available_seats, flight_number))
                
                conn.commit()
                
                # Insert into our in-memory AVL Tree
                new_booking = Booking(booking_id, user_id, flight_number, 'CONFIRMED', date_now)
                data_store.booking_root = data_store.booking_tree.insert(data_store.booking_root, booking_id, new_booking)
                
                # (Optional) If you later create a passengers table, you can save passenger_info['full_name'] and ['phone'] here!
                
                return True, f"Booking Confirmed! ID: {booking_id}"
                
            else:
                # 3. IF FLIGHT IS FULL: Add to Min-Heap Priority Queue (Waiting List)
                wait_id = f"WLT-{uuid.uuid4().hex[:8].upper()}"
                priority = datetime.datetime.now().timestamp()
                
                cursor.execute(
                    'INSERT INTO waiting_list (wait_id, user_id, flight_number, priority) VALUES (?, ?, ?, ?)',
                    (wait_id, user_id, flight_number, str(priority))
                )
                conn.commit()
                
                wait_data = {'wait_id': wait_id, 'user_id': user_id, 'flight_number': flight_number}
                data_store.waiting_list_pq.insert(wait_data, priority)
                
                return True, "Flight full. You have been added to the Priority Waiting List."
                
        except Exception as e:
            conn.rollback()
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def get_passenger_details(booking_id):
        """Returns dummy passenger details for the web API."""
        return {"full_name": "Passenger", "phone": "N/A"}