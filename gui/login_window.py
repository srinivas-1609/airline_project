import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService
from gui.admin_dashboard import AdminDashboard
from gui.passenger_dashboard import PassengerDashboard

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Reservation System - Login")
        self.root.geometry("400x420")
        self.root.configure(bg="#ffffff")
        
        # Title
        tk.Label(root, text="Airline Reservation System", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=25)
        
        # Username
        tk.Label(root, text="Username:", font=("Arial", 12), bg="#ffffff").pack()
        self.username_entry = tk.Entry(root, font=("Arial", 12), bg="#f1f1f1")
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(root, text="Password:", font=("Arial", 12), bg="#ffffff").pack()
        self.password_entry = tk.Entry(root, show="*", font=("Arial", 12), bg="#f1f1f1")
        self.password_entry.pack(pady=5)
        
        # Login Button
        tk.Button(root, text="Login", command=self.handle_login, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=15)
        
        tk.Label(root, text="Don't have an account?", bg="#ffffff", font=("Arial", 10)).pack(pady=5)
        
        # Register Button
        tk.Button(root, text="Register New Passenger", command=self.open_register_window, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        user = AuthService.login(username, password)
        
        if user:
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.open_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.\nPlease try again.")

    def open_dashboard(self, user):
        self.root.withdraw() 
        dash_window = tk.Toplevel(self.root)
        dash_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        
        if user['role'] == 'admin':
            AdminDashboard(dash_window, user, self.root)
        else:
            PassengerDashboard(dash_window, user, self.root)

    def open_register_window(self):
        """Opens a new window for passenger sign-up."""
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Passenger Registration")
        reg_win.geometry("350x350")
        reg_win.configure(bg="#f4f6f9")
        
        tk.Label(reg_win, text="Create Passenger Account", font=("Arial", 14, "bold"), bg="#f4f6f9").pack(pady=15)
        
        tk.Label(reg_win, text="Full Name:", bg="#f4f6f9", font=("Arial", 10)).pack()
        name_entry = tk.Entry(reg_win, font=("Arial", 10))
        name_entry.pack(pady=5)
        
        tk.Label(reg_win, text="Choose Username:", bg="#f4f6f9", font=("Arial", 10)).pack()
        user_entry = tk.Entry(reg_win, font=("Arial", 10))
        user_entry.pack(pady=5)
        
        tk.Label(reg_win, text="Choose Password:", bg="#f4f6f9", font=("Arial", 10)).pack()
        pass_entry = tk.Entry(reg_win, show="*", font=("Arial", 10))
        pass_entry.pack(pady=5)
        
        def submit_registration():
            name = name_entry.get().strip()
            username = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if not name or not username or not password:
                messagebox.showwarning("Input Error", "All fields are required!")
                return
                
            success, msg = AuthService.register_passenger(name, username, password)
            if success:
                messagebox.showinfo("Success", msg)
                reg_win.destroy() # Close registration window
            else:
                messagebox.showerror("Error", msg)
                
        tk.Button(reg_win, text="Sign Up", command=submit_registration, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=20)