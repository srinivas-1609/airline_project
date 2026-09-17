import tkinter as tk
from tkinter import messagebox
from gui.flight_search import FlightSearchWindow
from gui.route_search import RouteSearchWindow
from gui.my_bookings import MyBookingsWindow  # <-- Added Import

class PassengerDashboard:
    def __init__(self, root, user_data, login_window_root):
        self.root = root
        self.login_window_root = login_window_root
        self.user_data = user_data 
        self.root.title(f"Passenger Dashboard - {user_data.get('username', 'Passenger')}")
        self.root.geometry("600x450")
        self.root.configure(bg="#f4f6f9")

        # Header
        tk.Label(root, text="Passenger Portal", font=("Arial", 18, "bold"), bg="#f4f6f9").pack(pady=20)

        # Buttons
        tk.Button(root, text="Search & Book Flights", command=self.open_flight_search, width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        
        tk.Button(root, text="Find Shortest Route", command=self.open_route_search, width=30, height=2, bg="#9C27B0", fg="white", font=("Arial", 12)).pack(pady=10)
        
        # Connected the My Bookings button!
        tk.Button(root, text="My Bookings", command=self.open_my_bookings, width=30, height=2, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)
        
        # Logout Button
        tk.Button(root, text="Logout", command=self.logout, width=30, height=2, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=20)

    def open_flight_search(self):
        FlightSearchWindow(self.root, self.user_data)

    def open_route_search(self):
        RouteSearchWindow(self.root)

    def open_my_bookings(self):
        """Opens the window to view and cancel bookings."""
        MyBookingsWindow(self.root, self.user_data)

    def logout(self):
        self.root.destroy()
        self.login_window_root.deiconify()