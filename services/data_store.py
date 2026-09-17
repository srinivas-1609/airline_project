from data_structures.avl_tree import AVLTree
from data_structures.hash_table import HashTable
from data_structures.graph import Graph
from data_structures.priority_queue import PriorityQueue
import sqlite3
from database.database import get_connection
from models.flight import Flight
from models.booking import Booking

# Initialize all Data Structures
flight_tree = AVLTree()
booking_tree = AVLTree()
user_hash = HashTable()
airport_graph = Graph()
waiting_list_pq = PriorityQueue()

flight_root = None
booking_root = None

def build_expanded_graph():
    """Builds a realistic 15-airport network for Dijkstra's Algorithm."""
    # 15 Major Airports
    airports = ["DEL", "BOM", "BLR", "HYD", "MAA", "CCU", "AMD", "PNQ", "GOI", "JAI", "LKO", "ATQ", "TRV", "COK", "SXR"]
    for apt in airports:
        airport_graph.add_node(apt)
    
    # Connect them with distances (in km)
    edges = [
        ("DEL", "BOM", 1150), ("DEL", "BLR", 1740), ("DEL", "HYD", 1250), ("DEL", "MAA", 1760),
        ("DEL", "CCU", 1300), ("DEL", "SXR", 640), ("DEL", "JAI", 240), ("DEL", "LKO", 420),
        ("DEL", "ATQ", 400), ("BOM", "GOI", 400), ("BOM", "PNQ", 120), ("BOM", "BLR", 840), 
        ("BOM", "AMD", 440), ("BLR", "MAA", 290), ("BLR", "TRV", 500), ("BLR", "COK", 360), 
        ("HYD", "BLR", 500), ("HYD", "MAA", 520), ("HYD", "PNQ", 500), ("CCU", "MAA", 1360), 
        ("AMD", "JAI", 530), ("TRV", "COK", 190)
    ]
    # It's a two-way street (undirected graph)
    for src, dest, dist in edges:
        airport_graph.add_edge(src, dest, dist)
        airport_graph.add_edge(dest, src, dist)

def load_all_data():
    """Loads data from SQLite into the Data Structures."""
    global flight_root, booking_root
    
    # 1. Setup the huge Graph network first!
    build_expanded_graph()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Load Users into Hash Table
    cursor.execute('SELECT user_id, username, password, role, name FROM users')
    for row in cursor.fetchall():
        user_data = {'user_id': row[0], 'username': row[1], 'password': row[2], 'role': row[3], 'name': row[4]}
        user_hash.insert(row[1], user_data)
        
    # Load Flights into AVL Tree
    cursor.execute('SELECT * FROM flights')
    for r in cursor.fetchall():
        f = Flight(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9])
        flight_root = flight_tree.insert(flight_root, r[0], f)
        
    # Load Bookings into AVL Tree
    cursor.execute('SELECT * FROM bookings')
    for r in cursor.fetchall():
        b = Booking(r[0], r[1], r[2], r[3], r[4])
        booking_root = booking_tree.insert(booking_root, r[0], b)
        
    # Load Waiting List into Priority Queue
    cursor.execute('SELECT wait_id, user_id, flight_number, priority FROM waiting_list')
    for r in cursor.fetchall():
        waiting_list_pq.insert({'wait_id': r[0], 'user_id': r[1], 'flight_number': r[2]}, r[3])
        
    conn.close()
    print("All data successfully loaded from SQLite into Data Structures!")