import tkinter as tk
from tkinter import ttk, messagebox
from services.data_store import airport_graph
from algorithms.dijkstra import find_shortest_path

class RouteSearchWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Shortest Route Finder (Dijkstra)")
        self.root.geometry("500x400")
        self.root.configure(bg="#f9f9f9")

        tk.Label(self.root, text="Find Shortest Flight Route", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=20)

        # Get list of airports from our custom Graph
        self.airports = list(airport_graph.nodes.keys())
        
        if not self.airports:
            tk.Label(self.root, text="No airports available in the system.", bg="#f9f9f9").pack()
            return

        # Selection Frame
        frame = tk.Frame(self.root, bg="#f9f9f9")
        frame.pack(pady=10)

        # Source Airport Dropdown
        tk.Label(frame, text="Source Airport:", font=("Arial", 12), bg="#f9f9f9").grid(row=0, column=0, padx=10, pady=10)
        self.source_var = tk.StringVar()
        self.source_cb = ttk.Combobox(frame, textvariable=self.source_var, values=self.airports, state="readonly", font=("Arial", 12))
        self.source_cb.grid(row=0, column=1, padx=10, pady=10)

        # Destination Airport Dropdown
        tk.Label(frame, text="Destination Airport:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=0, padx=10, pady=10)
        self.dest_var = tk.StringVar()
        self.dest_cb = ttk.Combobox(frame, textvariable=self.dest_var, values=self.airports, state="readonly", font=("Arial", 12))
        self.dest_cb.grid(row=1, column=1, padx=10, pady=10)

        # Calculate Button
        tk.Button(self.root, text="Calculate Shortest Route", command=self.calculate_route, bg="#9C27B0", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

        # Result Display Area
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#f9f9f9", justify=tk.CENTER)
        self.result_label.pack(pady=10)

    def calculate_route(self):
        """Triggers Dijkstra's Algorithm and updates the GUI."""
        src = self.source_var.get()
        dest = self.dest_var.get()

        if not src or not dest:
            messagebox.showwarning("Input Error", "Please select both Source and Destination airports.")
            return
        if src == dest:
            messagebox.showinfo("Info", "Source and Destination are the same airport!")
            return

        # Call our custom Dijkstra implementation!
        path, distance = find_shortest_path(airport_graph, src, dest)

        if distance == float('inf'):
            self.result_label.config(text="No valid route found between these airports.", fg="red")
        else:
            # Format the output beautifully: HYD ➔ BLR ➔ DEL
            route_string = " ➔ ".join(path)
            self.result_label.config(
                text=f"Shortest Route:\n{route_string}\n\nTotal Distance: {distance} km", 
                fg="#2E7D32"
            )