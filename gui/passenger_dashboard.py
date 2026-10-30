import tkinter as tk
from gui.flight_search import FlightSearchWindow
from gui.route_search import RouteSearchWindow
from gui.my_bookings import MyBookingsWindow

class PassengerDashboard:
    def __init__(self, root, user, login_root=None):
        self.root = root
        self.user = user
        self.login_root = login_root
        self.root.title("Passenger Dashboard")
        self.root.geometry("500x400")

        welcome_name = self.user['name'] if self.user['role'] != 'guest' else 'Guest'
        tk.Label(self.root, text=f"Welcome, {welcome_name}!", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.root, text="View & Book Flights", command=self.open_flight_search, bg="#2196F3", fg="white", width=25, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Find Shortest Route", command=self.open_route_search, bg="#2196F3", fg="white", width=25, font=("Arial", 12)).pack(pady=10)
        
        if self.user['role'] != 'guest':
            tk.Button(self.root, text="My Bookings", command=self.open_my_bookings, bg="#2196F3", fg="white", width=25, font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="Logout" if self.user['role'] != 'guest' else "Back to Login", command=self.logout, bg="#f44336", fg="white", width=25, font=("Arial", 12)).pack(pady=10)

    def open_flight_search(self):
        FlightSearchWindow(self.root, self.user, self.login_root)

    def open_route_search(self):
        RouteSearchWindow(self.root, self.user)

    def open_my_bookings(self):
        MyBookingsWindow(self.root, self.user)

    def logout(self):
        self.root.destroy()
        if self.login_root:
            self.login_root.deiconify()