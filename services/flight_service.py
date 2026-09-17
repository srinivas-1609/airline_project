import sqlite3
from database.database import get_connection
from services import data_store
from models.flight import Flight

class FlightService:
    @staticmethod
    def add_flight(flight_number, airline, source, destination, date, dep_time, arr_time, seats, price):
        """Adds a flight to both SQLite and the AVL Tree."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO flights (flight_number, airline, source, destination, flight_date, dep_time, arr_time, total_seats, available_seats, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, airline, source, destination, date, dep_time, arr_time, seats, seats, price))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Error: Flight number already exists!"
        conn.close()

        f = Flight(flight_number, airline, source, destination, date, dep_time, arr_time, seats, seats, price)
        data_store.flight_root = data_store.flight_tree.insert(data_store.flight_root, flight_number, f)
        return True, "Flight added successfully!"

    @staticmethod
    def delete_flight(flight_number):
        """Deletes a flight from SQLite and the AVL Tree."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM flights WHERE flight_number = ?", (flight_number,))
        conn.commit()
        conn.close()

        # Delete from our AVL Tree using the custom delete method you wrote!
        data_store.flight_root = data_store.flight_tree.delete(data_store.flight_root, flight_number)
        return True, f"Flight {flight_number} deleted successfully!"

    @staticmethod
    def search_flight(flight_number):
        """Searches for a flight in O(log n) time using the AVL Tree."""
        node = data_store.flight_tree.search(data_store.flight_root, flight_number)
        if node:
            return node.data
        return None

    @staticmethod
    def get_all_flights():
        """Uses AVL Inorder Traversal to get all flights sorted by Flight Number."""
        nodes = data_store.flight_tree.inorder_traversal(data_store.flight_root)
        return [node[1] for node in nodes]