import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import numpy as np
import networkx as nx
from tkinter import ttk
import matplotlib.pyplot as plt
import random

from ant_colony import ant_colony_algorithm_with_2opt 


class AddEdgeDialog(simpledialog.Dialog):
    def __init__(self, parent, vertices):
        self.vertices = vertices
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="Start Vertex:").grid(row=0, column=0)
        tk.Label(master, text="End Vertex:").grid(row=1, column=0)
        tk.Label(master, text="Edge Weight:").grid(row=2, column=0)

        self.start_vertex_entry = tk.Entry(master)
        self.end_vertex_entry = tk.Entry(master)
        self.edge_weight_entry = tk.Entry(master)

        self.start_vertex_entry.grid(row=0, column=1)
        self.end_vertex_entry.grid(row=1, column=1)
        self.edge_weight_entry.grid(row=2, column=1)

        return self.start_vertex_entry

    def apply(self):
        try:
            start_vertex = int(self.start_vertex_entry.get())
            end_vertex = int(self.end_vertex_entry.get())
            edge_weight = float(self.edge_weight_entry.get())

            if start_vertex < 1 or start_vertex > len(self.vertices) or end_vertex < 1 or end_vertex > len(self.vertices):
                raise ValueError("Invalid vertex indices.")

            self.result = (start_vertex, end_vertex, edge_weight)
        except ValueError as e:
            messagebox.showinfo("Error", str(e))
            self.result = None


class GraphApp:
    def __init__(self, master):
        self.master = master
        self.canvas_width = 600
        self.canvas_height = 400

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.vertices = []
        self.edges = []

        self.vertex_count = 0
        self.graph = nx.DiGraph()

        self.canvas.bind("<Button-1>", self.add_vertex)

        self.treeview = ttk.Treeview(self.graph_frame, columns=("Start", "End", "Weight"), show='headings')
        self.treeview.heading("Start", text="Start", anchor=tk.CENTER)
        self.treeview.heading("End", text="End", anchor=tk.CENTER)
        self.treeview.heading("Weight", text="Weight", anchor=tk.CENTER)
        self.treeview.column("Start", anchor=tk.CENTER)
        self.treeview.column("End", anchor=tk.CENTER)
        self.treeview.column("Weight", anchor=tk.CENTER)
        self.treeview.pack(expand=True, fill=tk.BOTH)

        self.add_edge_button = tk.Button(self.graph_frame, text="Add Weighted Edge", command=self.add_weighted_edge)
        self.add_edge_button.pack()

        self.calculate_mst_button = tk.Button(self.graph_frame, text="Calculate MST", command=self.calculate_hamilton_cycle)
        self.calculate_mst_button.pack()

    def add_vertex(self, event):
        x, y = event.x, event.y
        self.vertex_count += 1
        vertex_id = self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill="black")
        label_id = self.canvas.create_text(x, y, text=str(self.vertex_count), font=("Arial", 12), fill="white")
        self.vertices.append((x, y, self.vertex_count, vertex_id, label_id))

    def add_weighted_edge(self):
        if len(self.vertices) < 2:
            messagebox.showinfo("Error", "At least 2 vertices are needed to create an edge.")
            return

        dialog = AddEdgeDialog(self.master, self.vertices)
        if dialog.result:
            start_vertex, end_vertex, edge_weight = dialog.result
            self.graph.add_weighted_edges_from([(start_vertex, end_vertex, edge_weight)])

            x1, y1, _, _, _ = self.vertices[start_vertex - 1]
            x2, y2, _, _, _ = self.vertices[end_vertex - 1]
            angle = math.atan2(y2 - y1, x2 - x1)
            arrowhead_length = 5  
            vertex_radius = 10  
            arrowhead_x = x2 - (vertex_radius + arrowhead_length) * math.cos(angle)  
            arrowhead_y = y2 - (vertex_radius + arrowhead_length) * math.sin(angle)  
            arrowhead_start_x = x1 + (vertex_radius + arrowhead_length) * math.cos(angle)
            arrowhead_start_y = y1 + (vertex_radius + arrowhead_length) * math.sin(angle)
            edge_id = self.canvas.create_line(arrowhead_start_x, arrowhead_start_y, arrowhead_x, arrowhead_y, arrow=tk.LAST, fill="red", width=3)
            self.edges.append(((x1, y1), (x2, y2), edge_weight, edge_id))
            self.graph.add_weighted_edges_from([(start_vertex, end_vertex, edge_weight)])

            self.treeview.insert("", tk.END, values=(start_vertex, end_vertex, edge_weight))

    def calculate_hamilton_cycle(self):
        best_solution, best_cost = ant_colony_algorithm_with_2opt(self.graph)
        hamilton_cycle_info = f"Shortest Hamilton Cycle (Length: {best_cost}): {best_solution}"
        print(hamilton_cycle_info)
        
        hamilton_window = tk.Toplevel()
        hamilton_window.title("Shortest Hamilton Cycle")
        hamilton_window.geometry("800x600")
        
        hamilton_canvas = tk.Canvas(hamilton_window, width=self.canvas_width, height=self.canvas_height, bg="white")
        hamilton_canvas.pack()

        for x, y, vertex_id, _, _ in self.vertices:
            hamilton_canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill="black")
            hamilton_canvas.create_text(x, y, text=str(vertex_id), font=("Arial", 12), fill="white")

        for u, v in zip(best_solution, best_solution[1:] + [best_solution[0]]):
            x1, y1, _, _, _ = self.vertices[u - 1]
            x2, y2, _, _, _ = self.vertices[v - 1]
            hamilton_canvas.create_line(x1, y1, x2, y2, fill="blue", width=3)


def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()