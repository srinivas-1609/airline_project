import tkinter as tk
from tkinter import ttk, messagebox
from services.flight_service import FlightService
from services.reservation_service import ReservationService

class FlightSearchWindow:
    def __init__(self, root, user_data):
        self.root = tk.Toplevel(root)
        self.root.title("Search and Book Flights")
        self.root.geometry("800x450")
        self.user_data = user_data

        tk.Label(self.root, text="Available Flights", font=("Arial", 16, "bold")).pack(pady=10)
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)       
        tk.Label(search_frame, text="Search by Flight Number:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)       
        tk.Button(search_frame, text="Search Flight", command=self.search_flight, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_all_flights, bg="#757575", fg="white").pack(side=tk.LEFT, padx=5)
        columns = ("Flight No", "Airline", "From", "To", "Date", "Seats", "Price")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.X, padx=20)
        tk.Button(self.root, text="Book Flight", command=self.book_flight, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.load_all_flights()

    def load_all_flights(self):
        """Fetches all flights using Inorder Traversal of the AVL Tree."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        flights = FlightService.get_all_flights()
        for f in flights:
            self.tree.insert("", tk.END, values=(f.flight_number, f.airline, f.source, f.destination, f.flight_date, f.available_seats, f.price))

    def search_flight(self):
        """Searches for a specific flight using AVL Tree search (O(log n))."""
        flight_num = self.search_entry.get().strip().upper()
        if not flight_num:
            messagebox.showwarning("Input Error", "Please enter a Flight Number.")
            return

        flight = FlightService.search_flight(flight_num)
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if flight:
            self.tree.insert("", tk.END, values=(flight.flight_number, flight.airline, flight.source, flight.destination, flight.flight_date, flight.available_seats, flight.price))
        else:
            messagebox.showinfo("Not Found", "No flight found with that number.")

    def book_flight(self):
        """Books a ticket and links it to the database & Booking AVL Tree."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a flight from the list to book.")
            return

        flight_num = self.tree.item(selected_item)['values'][0]
        
        confirm = messagebox.askyesno("Confirm Booking", f"Do you want to book a ticket for Flight {flight_num}?")
        if confirm:
            success, message = ReservationService.book_ticket(self.user_data['user_id'], flight_num)
            if success:
                messagebox.showinfo("Booking Success", message)
            else:
                messagebox.showinfo("Booking Status", message) 
            self.load_all_flights()