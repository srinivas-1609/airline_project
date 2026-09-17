import tkinter as tk
from gui.flight_management import FlightManagementWindow
from gui.admin_bookings import AdminBookingsWindow # <-- Added import

class AdminDashboard:
    def __init__(self, root, user_data, login_window_root):
        self.root = root
        self.login_window_root = login_window_root
        self.root.title(f"Admin Dashboard - {user_data.get('username', 'Admin')}")
        self.root.geometry("600x400")
        self.root.configure(bg="#f4f6f9")

        # Header
        tk.Label(root, text="Admin Control Panel", font=("Arial", 18, "bold"), bg="#f4f6f9").pack(pady=20)

        # Buttons
        tk.Button(root, text="Flight Management", command=self.open_flight_management, width=30, height=2, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)
        
        # Connected the Bookings & Revenue button!
        tk.Button(root, text="View All Bookings & Revenue", command=self.open_admin_bookings, width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        
        # Logout Button
        tk.Button(root, text="Logout", command=self.logout, width=30, height=2, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=20)

    def open_flight_management(self):
        FlightManagementWindow(self.root)

    def open_admin_bookings(self):
        """Opens the window to view all system bookings and revenue."""
        AdminBookingsWindow(self.root)

    def logout(self):
        self.root.destroy()
        self.login_window_root.deiconify()