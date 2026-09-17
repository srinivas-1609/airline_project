import tkinter as tk
from tkinter import ttk
from services import data_store
from services.flight_service import FlightService

class AdminBookingsWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Admin - All Bookings & Revenue Analysis")
        self.root.geometry("800x500")
        self.root.configure(bg="#f4f6f9")

        tk.Label(self.root, text="System Bookings & Revenue", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=15)

        # Revenue Display Area
        self.revenue_label = tk.Label(self.root, text="Calculating Revenue...", font=("Arial", 14, "bold"), fg="#2E7D32", bg="#f4f6f9")
        self.revenue_label.pack(pady=5)

        # Table for displaying ALL bookings
        columns = ("Booking ID", "User ID", "Flight No", "Status", "Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        
        for col_name in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=120, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.X, padx=20)

        self.load_all_data_and_revenue()

    def load_all_data_and_revenue(self):
        """Fetches all bookings from the AVL Tree and calculates total revenue."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Get all bookings using Inorder Traversal of the Booking AVL Tree
        all_bookings_nodes = data_store.booking_tree.inorder_traversal(data_store.booking_root)
        
        total_revenue = 0.0
        active_bookings = 0
        cancelled_bookings = 0
        
        for node in all_bookings_nodes:
            b = node[1] # The actual Booking object
            self.tree.insert("", tk.END, values=(b.booking_id, b.user_id, b.flight_number, b.status, b.booking_date))
            
            if b.status == 'CONFIRMED':
                active_bookings += 1
                # Find the flight to get its price
                flight = FlightService.search_flight(b.flight_number)
                if flight:
                    total_revenue += flight.price
            else:
                cancelled_bookings += 1

        # Update the Revenue Label
        stats_text = (f"Total Revenue: ₹{total_revenue:,.2f}  |  "
                      f"Active Tickets: {active_bookings}  |  "
                      f"Cancelled: {cancelled_bookings}")
        self.revenue_label.config(text=stats_text)