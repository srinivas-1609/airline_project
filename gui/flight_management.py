import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import datetime
from services.flight_service import FlightService
from services.data_store import airport_graph

class CalendarDialog(tk.Toplevel):
    """A custom Date Picker popup using 0 external libraries!"""
    def __init__(self, parent, entry_widget):
        super().__init__(parent)
        self.title("Select Date")
        self.geometry("260x220")
        self.entry_widget = entry_widget
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.setup_ui()

    def setup_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        header = tk.Frame(self)
        header.pack(pady=5)
        tk.Button(header, text="<", command=self.prev_month).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text=f"{calendar.month_name[self.month]} {self.year}", font=("Arial", 10, "bold"), width=12).pack(side=tk.LEFT)
        tk.Button(header, text=">", command=self.next_month).pack(side=tk.LEFT, padx=5)

        cal_frame = tk.Frame(self)
        cal_frame.pack()
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day, font=("Arial", 8, "bold")).grid(row=0, column=i, padx=2, pady=2)

        cal = calendar.monthcalendar(self.year, self.month)
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day != 0:
                    tk.Button(cal_frame, text=str(day), width=3, command=lambda d=day: self.select_date(d)).grid(row=row_idx+1, column=col_idx, pady=1)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.setup_ui()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.setup_ui()

    def select_date(self, day):
        date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        self.entry_widget.config(state=tk.NORMAL)
        self.entry_widget.delete(0, tk.END)
        self.entry_widget.insert(0, date_str)
        self.entry_widget.config(state="readonly")
        self.destroy()


class FlightManagementWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Admin - Pro Flight Management")
        self.root.geometry("850x650")

        tk.Label(self.root, text="Flight Management", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        labels = ["Flight No:", "Airline:", "Source:", "Dest:", "Date:", "Dep Time:", "Arr Time:", "Seats:", "Price:"]
        self.entries = {}

        valid_airports = list(airport_graph.nodes.keys())
        valid_airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]
        time_slots = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]

        row, col = 0, 0
        for label in labels:
            tk.Label(form_frame, text=label).grid(row=row, column=col, padx=5, pady=5, sticky=tk.E)
            
            # SMART INPUTS BASED ON LABEL
            if label == "Airline:":
                entry = ttk.Combobox(form_frame, values=valid_airlines, state="readonly", width=12)
            elif label in ["Source:", "Dest:"]:
                entry = ttk.Combobox(form_frame, values=valid_airports, state="readonly", width=12)
            elif label in ["Dep Time:", "Arr Time:"]:
                entry = ttk.Combobox(form_frame, values=time_slots, state="readonly", width=12)
            elif label == "Date:":
                # Create a mini frame just for the Date Entry + Calendar Button
                date_frame = tk.Frame(form_frame)
                date_frame.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
                
                entry = tk.Entry(date_frame, width=10)
                entry.insert(0, "YYYY-MM-DD")
                entry.config(state="readonly")
                entry.pack(side=tk.LEFT)
                
                tk.Button(date_frame, text="📅", command=lambda e=entry: CalendarDialog(self.root, e)).pack(side=tk.LEFT, padx=2)
                self.entries[label] = entry
                col += 2
                continue # Skip standard placement since we used the date_frame
            else:
                entry = tk.Entry(form_frame, width=15)
                
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            self.entries[label] = entry
            
            col += 2
            if col >= 6: 
                col = 0
                row += 1

        tk.Button(form_frame, text="Add New Flight", command=self.add_flight, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=row+1, column=0, columnspan=6, pady=15)

        columns = ("Flight No", "Airline", "From", "To", "Date", "Seats", "Price")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        
        for col_name in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=100, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.X, padx=20)

        tk.Button(self.root, text="Delete Selected Flight", command=self.delete_flight, bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        self.load_all_flights()

    def load_all_flights(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        flights = FlightService.get_all_flights()
        for f in flights:
            self.tree.insert("", tk.END, values=(f.flight_number, f.airline, f.source, f.destination, f.flight_date, f.total_seats, f.price))

    def add_flight(self):
        try:
            f_no = self.entries["Flight No:"].get().strip().upper()
            airline = self.entries["Airline:"].get()
            src = self.entries["Source:"].get()
            dest = self.entries["Dest:"].get()
            date = self.entries["Date:"].get()
            dep = self.entries["Dep Time:"].get()
            arr = self.entries["Arr Time:"].get()
            
            # Error checking
            if not f_no or not airline or not src or not dest or date == "YYYY-MM-DD" or not dep or not arr:
                messagebox.showerror("Error", "Please fill in all dropdowns and fields.")
                return
            if src == dest:
                messagebox.showerror("Error", "Source and Destination cannot be the same airport.")
                return
                
            seats = int(self.entries["Seats:"].get().strip())
            price = float(self.entries["Price:"].get().strip())

            success, msg = FlightService.add_flight(f_no, airline, src, dest, date, dep, arr, seats, price)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_all_flights()
            else:
                messagebox.showerror("Error", msg)

        except ValueError:
            messagebox.showerror("Error", "Seats and Price must be valid numbers.")

    def delete_flight(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a flight to delete.")
            return

        flight_num = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to permanently delete flight {flight_num}?")
        if confirm:
            success, msg = FlightService.delete_flight(flight_num)
            messagebox.showinfo("Deleted", msg)
            self.load_all_flights()