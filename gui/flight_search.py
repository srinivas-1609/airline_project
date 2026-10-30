import tkinter as tk
from tkinter import ttk, messagebox
from services.flight_service import FlightService
from services.reservation_service import ReservationService

class FlightSearchWindow:
    def __init__(self, root, user, login_root=None):
        self.root = tk.Toplevel(root)
        self.root.title("Search & Book Flights")
        self.root.geometry("800x550")
        self.user = user
        self.login_root = login_root

        # --- NEW BACK BUTTON ---
        tk.Button(self.root, text="⬅ Back to Dashboard", command=self.root.destroy, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=10, pady=10)

        tk.Label(self.root, text="Available Flights", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("Flight No", "Airline", "From", "To", "Date", "Seats", "Price")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.X, padx=20)

        tk.Button(self.root, text="Book Selected Flight", command=self.initiate_booking, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

        self.load_flights()

    def load_flights(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        flights = FlightService.get_all_flights()
        for f in flights:
            self.tree.insert("", tk.END, values=(f.flight_number, f.airline, f.source, f.destination, f.flight_date, f.available_seats, f.price))

    def initiate_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a flight to book.")
            return

        if self.user['role'] == 'guest':
            messagebox.showwarning("Login Required", "You must log in to book a flight. Redirecting to login.")
            self.root.destroy()
            if self.login_root:
                # Closes the dashboard and brings back the login screen
                self.root.master.destroy() 
                self.login_root.deiconify()
            return

        flight_num = self.tree.item(selected)['values'][0]
        price = self.tree.item(selected)['values'][6]
        self.show_booking_form(flight_num, price)

    def show_booking_form(self, flight_num, price):
        popup = tk.Toplevel(self.root)
        popup.title("Confirm Booking")
        popup.geometry("300x300")

        tk.Label(popup, text=f"Booking: {flight_num}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(popup, text=f"Total Price: ₹{price}", font=("Arial", 12, "bold"), fg="green").pack(pady=5)

        tk.Label(popup, text="Passenger Name:").pack()
        name_entry = tk.Entry(popup)
        name_entry.insert(0, self.user['name'])
        name_entry.pack(pady=5)

        tk.Label(popup, text="Phone Number:").pack()
        phone_entry = tk.Entry(popup)
        phone_entry.pack(pady=5)

        def confirm():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name or not phone:
                messagebox.showwarning("Input Error", "Name and Phone are required.")
                return
                
            passenger_info = {'full_name': name, 'phone': phone}
            success, msg = ReservationService.book_ticket(self.user['user_id'], flight_num, passenger_info)
            
            if success:
                messagebox.showinfo("Success", "Booking Confirmed!")
                popup.destroy()
                self.load_flights()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(popup, text="Confirm & Pay", command=confirm, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20)