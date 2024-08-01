import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from flujoMaximo import MaxFlow

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafo")

        self.graph = nx.DiGraph()
        self.positions = {}
        self.edges = []

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack(pady=20)

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.add_edge)

        self.frame = ttk.Frame(root, style="TFrame")
        self.frame.pack()

        self.icons = self.load_icons()

        self.btn_result = ttk.Button(self.frame, image=self.icons['icon1'], style="TButton", command=self.shortest_path)
        self.btn_result.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_max_flow = ttk.Button(self.frame, image=self.icons['icon4'], style="TButton", command=self.max_flow)
        self.btn_max_flow.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_clear = ttk.Button(self.frame, image=self.icons['icon2'], style="TButton", command=self.clear_all)
        self.btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_delete_node = ttk.Button(self.frame, image=self.icons['icon3'], style="TButton", command=self.delete_node)
        self.btn_delete_node.pack(side=tk.LEFT, padx=5, pady=5)

        self.start_node = None
        self.end_node = None

    def load_icons(self):
        icons = {}
        icons['icon1'] = ImageTk.PhotoImage(Image.open("assets/images/icon1.png").resize((30, 30)))
        icons['icon2'] = ImageTk.PhotoImage(Image.open("assets/images/icon2.png").resize((30, 30)))
        icons['icon3'] = ImageTk.PhotoImage(Image.open("assets/images/icon3.png").resize((30, 30)))
        icons['icon4'] = ImageTk.PhotoImage(Image.open("assets/images/icon4.png").resize((30, 30)))
        return icons

    def add_node(self, event):
        node_id = simpledialog.askstring("Input", "Ingrese el nombre del nodo:", parent=self.root)
        if node_id:
            x, y = event.x, event.y
            self.positions[node_id] = (x, y)
            self.graph.add_node(node_id)
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="skyblue", outline="black")
            self.canvas.create_text(x, y, text=node_id, font=("Arial", 12))

    def add_edge(self, event):
        if not self.start_node:
            for node, pos in self.positions.items():
                if abs(pos[0] - event.x) < 10 and abs(pos[1] - event.y) < 10:
                    self.start_node = node
                    break
        else:
            for node, pos in self.positions.items():
                if abs(pos[0] - event.x) < 10 and abs(pos[1] - event.y) < 10:
                    self.end_node = node
                    break
            if self.start_node and self.end_node:
                distance = simpledialog.askfloat("Input", f"Ingrese la distancia entre {self.start_node} y {self.end_node}:", parent=self.root)
                if distance:
                    self.graph.add_edge(self.start_node, self.end_node, weight=distance)
                    self.edges.append((self.start_node, self.end_node, distance))
                    x1, y1 = self.positions[self.start_node]
                    x2, y2 = self.positions[self.end_node]
                    self.canvas.create_line(x1, y1, x2, y2, fill="black")
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(distance), font=("Arial", 10))
                self.start_node = None
                self.end_node = None

    def shortest_path(self):
        start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:", parent=self.root)
        end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:", parent=self.root)
        if start_node and end_node:
            try:
                path = nx.dijkstra_path(self.graph, source=start_node, target=end_node)
                path_edges = list(zip(path, path[1:]))
                self.plot_graph(path_edges)
            except nx.NetworkXNoPath:
                messagebox.showerror("Error", "No existe una ruta entre los nodos especificados")

    def plot_graph(self, path_edges):
        plt.figure()
        pos = self.positions
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=15, font_color='black', font_weight='bold', edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='r', width=2)
        plt.title("Ruta más corta")
        plt.show()

    def clear_all(self):
        self.graph.clear()
        self.positions.clear()
        self.edges.clear()
        self.canvas.delete("all")

    def delete_node(self):
        node_id = simpledialog.askstring("Input", "Ingrese el nombre del nodo a borrar:", parent=self.root)
        if node_id:
            if node_id in self.graph:
                self.graph.remove_node(node_id)
                self.positions.pop(node_id, None)
                self.canvas.delete("all")
                for node, pos in self.positions.items():
                    self.canvas.create_oval(pos[0]-10, pos[1]-10, pos[0]+10, pos[1]+10, fill="skyblue", outline="black")
                    self.canvas.create_text(pos[0], pos[1], text=node, font=("Arial", 12))
                for edge in self.graph.edges(data=True):
                    x1, y1 = self.positions[edge[0]]
                    x2, y2 = self.positions[edge[1]]
                    self.canvas.create_line(x1, y1, x2, y2, fill="black")
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(edge[2]['weight']), font=("Arial", 10))

    #PIDE LOS DATOS Y LLAMA A LA LOGICA DE LA CLASE flujoMaximo
    def max_flow(self):
        start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:", parent=self.root)
        end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:", parent=self.root)
        if start_node and end_node:
            try:
                max_flow_calc = MaxFlow(self.graph)
                flow_value, flow_dict = max_flow_calc.max_flow(start_node, end_node)
                max_flow_calc.plot_graph_with_flow(flow_dict)
                messagebox.showinfo("Resultado", f"Flujo máximo: {flow_value}")
            except nx.NetworkXUnbounded:
                messagebox.showerror("Error", "El grafo contiene un camino con capacidad infinita")
            except nx.NetworkXNoPath:
                messagebox.showerror("Error", "No existe una ruta entre los nodos especificados")
