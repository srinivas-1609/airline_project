import tkinter as tk
from tkinter import ttk, messagebox
from services.cancellation_service import CancellationService

class MyBookingsWindow:
    def __init__(self, root, user_data):
        self.root = tk.Toplevel(root)
        self.root.title("My Bookings")
        self.root.geometry("700x400")
        self.user_data = user_data

        # FIX: Changed ['name'] to .get('username')
        tk.Label(self.root, text=f"{self.user_data.get('username', 'Your')}'s Tickets", font=("Arial", 16, "bold")).pack(pady=15)

        # Table for displaying bookings
        columns = ("Booking ID", "Flight No", "Status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        
        for col_name in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=150, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.X, padx=20)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh List", command=self.load_my_bookings, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel Selected Ticket", command=self.cancel_ticket, bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        self.load_my_bookings()

    def load_my_bookings(self):
        """Fetches and displays the user's bookings."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        bookings = CancellationService.get_user_bookings(self.user_data['user_id'])
        
        for b in bookings:
            self.tree.insert("", tk.END, values=(b.booking_id, b.flight_number, b.status))

    def cancel_ticket(self):
        """Cancels the selected ticket."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a booking to cancel.")
            return

        booking_id = self.tree.item(selected_item)['values'][0]
        current_status = self.tree.item(selected_item)['values'][2]
        
        if current_status == 'CANCELLED':
            messagebox.showinfo("Info", "This ticket is already cancelled.")
            return
            
        confirm = messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel booking {booking_id}?")
        if confirm:
            success, msg = CancellationService.cancel_booking(booking_id)
            if success:
                messagebox.showinfo("Cancelled", msg)
                self.load_my_bookings() # Refresh the table
            else:
                messagebox.showerror("Error", msg)