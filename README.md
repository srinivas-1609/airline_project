# Airline Reservation System (DSA Implementation)

A comprehensive, academic-grade Airline Reservation System built entirely in Python using core Data Structures and Algorithms (DSA) from scratch, integrated with an SQLite persistent database and a Tkinter GUI.

## 🚀 Features & DSA Mapping

This project demonstrates the practical application of advanced data structures to solve real-world software engineering problems without relying on external libraries for core logic.

1. **User Authentication (Hash Tables)**
   - **Data Structure:** Hash Table with Chaining (Linked Lists).
   - **Use Case:** Stores user credentials for O(1) average time complexity logins and secure credential verification.

2. **Flight & Booking Management (AVL Trees)**
   - **Data Structure:** AVL Tree (Self-Balancing Binary Search Tree).
   - **Use Case:** Stores flights and bookings in memory. Ensures O(log n) time complexity for searching, inserting, and deleting flights or tickets, preventing performance degradation.

3. **Shortest Route Finder (Graphs & Dijkstra's Algorithm)**
   - **Data Structure:** Adjacency List Graph.
   - **Algorithm:** Dijkstra's Shortest Path Algorithm.
   - **Use Case:** Calculates the shortest total distance and exact flight path between any two airports in the network.

4. **Waiting List Management (Priority Queue / Min-Heap)**
   - **Data Structure:** Min-Heap (Array-based).
   - **Use Case:** When a flight is full, users are added to a waiting list based on priority (timestamp). If a ticket is cancelled, the Min-Heap pops the highest-priority user in O(log n) time and automatically books their ticket.

## 📁 Project Architecture

* `algorithms/` - Contains Dijkstra's algorithm logic.
* `data_structures/` - Contains from-scratch implementations of AVL Tree, Graph, Hash Table, and Priority Queue.
* `database/` - SQLite database initialization and connection handling.
* `models/` - Object-oriented data classes (Flight, Booking, Passenger).
* `services/` - Business logic linking the GUI, Database, and in-memory Data Structures.
* `gui/` - Modular Tkinter graphical user interfaces (Dashboards, Search, Management).
* `main.py` - Application entry point.

## 🛠️ How to Run
1. Ensure Python 3.x is installed.
2. Navigate to the project root directory.
3. Run the application: `python main.py`
4. Use `admin` / `admin123` for Admin access, or `johndoe` / `pass123` for Passenger access.