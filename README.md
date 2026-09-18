# Airline Reservation System (DSA Implementation)

A comprehensive, academic-grade Airline Reservation System built entirely in Python using core Data Structures and Algorithms (DSA) from scratch, integrated with an SQLite persistent database, a Tkinter GUI, and a **live web application** (FastAPI backend + modern single-page frontend).

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

## 🌐 Run as a Live Website (Recommended)

The web version serves the same DSA-powered engine over a REST API with a modern browser UI.

1. Ensure Python 3.x with `fastapi` and `uvicorn` installed: `pip install fastapi uvicorn`
2. Navigate to the project root directory.
3. Start the server: `python -m uvicorn web_api:app --host 127.0.0.1 --port 8000`
4. Open **http://127.0.0.1:8000** in your browser.
5. Log in with `admin` / `admin123` (Admin Panel) or `johndoe` / `pass123` (Passenger), or create a new account.

On first launch the system seeds ~70 upcoming flights across a 15-airport network so the site is instantly usable.

### Web Features
- Flight search by route and date, one-click booking, and a Dijkstra-powered shortest route finder
- Passenger dashboard with booking history and cancellation (auto-promotes waitlisted passengers via the Min-Heap)
- Admin panel: live stats, add/delete flights, all bookings, and the priority waiting list

### API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login`, `/api/register` | Authentication |
| GET | `/api/flights`, `/api/flights/{fn}` | Search flights (AVL tree) |
| GET | `/api/route?from=X&to=Y` | Shortest path (Dijkstra) |
| POST/GET/DELETE | `/api/bookings` | Book, list, cancel (Min-Heap waitlist) |
| GET/POST/DELETE | `/api/admin/*` | Admin: stats, flights, bookings, waitlist |

Interactive API docs are available at `/docs` when the server is running.

## 🖥️ Run the Desktop GUI (Legacy)
1. Ensure Python 3.x is installed.
2. Navigate to the project root directory.
3. Run the application: `python main.py`
4. Use `admin` / `admin123` for Admin access, or `johndoe` / `pass123` for Passenger access.