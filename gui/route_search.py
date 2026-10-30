import tkinter as tk
from tkinter import ttk, messagebox
from services.data_store import airport_graph
from algorithms.dijkstra import find_shortest_path

class RouteSearchWindow:
    def __init__(self, root, user):
        self.root = tk.Toplevel(root)
        self.root.title("Shortest Route Finder")
        self.root.geometry("600x550")
        self.user = user

        tk.Button(self.root, text="⬅ Back to Dashboard", command=self.root.destroy, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(self.root, text="Shortest Path Finder", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        airports = sorted(list(airport_graph.nodes.keys()))

        tk.Label(form_frame, text="From:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.src_combo = ttk.Combobox(form_frame, values=airports, state="readonly", font=("Arial", 12))
        self.src_combo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="To:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.dest_combo = ttk.Combobox(form_frame, values=airports, state="readonly", font=("Arial", 12))
        self.dest_combo.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(form_frame, text="Find Route", command=self.calculate_route, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2, pady=20)

        self.result_text = tk.Text(self.root, height=12, width=60, font=("Arial", 12), bg="#f4f6f9", state=tk.DISABLED, padx=10, pady=10)
        self.result_text.pack(pady=10)

    def calculate_route(self):
        src = self.src_combo.get()
        dest = self.dest_combo.get()

        if not src or not dest:
            messagebox.showerror("Error", "Please select both Source and Destination.")
            return
        if src == dest:
            messagebox.showerror("Error", "Source and Destination cannot be the same.")
            return

        path, distance = find_shortest_path(airport_graph, src, dest)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if not path or distance == float('inf'):
            self.result_text.insert(tk.END, f"No route available between {src} and {dest}.")
        else:
            stops = len(path) - 2
            intermediate = path[1:-1]
            
            result = f"Source: {src}\n"
            result += f"Destination: {dest}\n"
            result += f"Total Distance: {distance} km\n"
            result += f"Total Layovers: {stops}\n\n"
            
            if stops > 0:
                result += f"Intermediate Stations: {' ➔ '.join(intermediate)}\n\n"
            else:
                result += "Intermediate Stations: Direct Flight (No stops)\n\n"
                
            result += f"Full Flight Path:\n{' ➔ '.join(path)}"
            
            self.result_text.insert(tk.END, result)
            
        self.result_text.config(state=tk.DISABLED)