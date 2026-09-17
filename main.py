import tkinter as tk
from database.database import setup_database, insert_sample_data
from services.data_store import load_all_data
from gui.login_window import LoginWindow

def initialize_system():
    print("Initializing Airline Reservation System...")
    # 1. Ensure database exists and has dummy data
    setup_database()
    insert_sample_data()
    
    # 2. Load all SQLite data into our AVL Trees, Hash Table, and Graph
    load_all_data()
    print("System ready!")

if __name__ == "__main__":
    # Run the background setup
    initialize_system()
    
    # Launch the GUI
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()