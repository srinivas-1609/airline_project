from database.database import get_connection
from services import data_store
from services.flight_service import FlightService
import uuid
from models.booking import Booking

class CancellationService:
    @staticmethod
    def cancel_booking(booking_id):
        """Cancels a booking and automatically promotes a waiting list passenger using our Priority Queue."""
        
        # 1. Find the booking in our Booking AVL Tree (O(log n))
        booking_node = data_store.booking_tree.search(data_store.booking_root, booking_id)
        if not booking_node:
            return False, "Error: Booking not found in system."
            
        booking = booking_node.data
        if booking.status == 'CANCELLED':
            return False, "This booking is already cancelled."

        flight = FlightService.search_flight(booking.flight_number)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # 2. Cancel the current booking in SQLite and AVL Tree
        cursor.execute("UPDATE bookings SET status = 'CANCELLED' WHERE booking_id = ?", (booking_id,))
        booking.status = 'CANCELLED'
        
        message = f"Booking {booking_id} cancelled successfully.\n"

        # 3. ACTUAL DSA IMPLEMENTATION: Pop from our Custom Priority Queue!
        waiting_passenger_data = data_store.waiting_list_pq.pop_for_flight(flight.flight_number)

        if waiting_passenger_data:
            # We found someone in the Min-Heap waiting for this flight!
            wait_id = waiting_passenger_data['wait_id']
            next_user_id = waiting_passenger_data['user_id']
            
            # Generate a new booking for them
            new_booking_id = "BKG-" + str(uuid.uuid4())[:8].upper()
            
            # Insert their new booking into SQLite
            cursor.execute('INSERT INTO bookings (booking_id, user_id, flight_number, status) VALUES (?, ?, ?, ?)',
                           (new_booking_id, next_user_id, flight.flight_number, 'CONFIRMED'))
            
            # Delete their old waiting list record from SQLite
            cursor.execute('DELETE FROM waiting_list WHERE wait_id = ?', (wait_id,))
            
            # Insert their new booking into the Booking AVL Tree
            new_b = Booking(new_booking_id, next_user_id, flight.flight_number, 'CONFIRMED', 'Just Now')
            data_store.booking_root = data_store.booking_tree.insert(data_store.booking_root, new_booking_id, new_b)
            
            message += f"Good news! A waiting list passenger was automatically promoted and booked using the Priority Queue!"
        else:
            # If no one is waiting in the queue, just increase the available seats
            if flight:
                flight.available_seats += 1
                cursor.execute("UPDATE flights SET available_seats = ? WHERE flight_number = ?", 
                               (flight.available_seats, flight.flight_number))
                message += "Seat has been added back to available inventory."

        conn.commit()
        conn.close()
        
        return True, message

    @staticmethod
    def get_user_bookings(user_id):
        all_bookings_nodes = data_store.booking_tree.inorder_traversal(data_store.booking_root)
        user_bookings = []
        for node in all_bookings_nodes:
            booking = node[1]
            if booking.user_id == user_id:
                user_bookings.append(booking)
        return user_bookings