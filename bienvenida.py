import tkinter as tk
from tkinter import ttk
from styles import set_canvas_background

class WelcomeScreen:
    def __init__(self, root, start_callback):
        self.root = root
        self.root.title("DijkstraDrawer")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(expand=True, fill='both')

        set_canvas_background(self.canvas, "assets/images/frame.png")

        self.frame = ttk.Frame(self.canvas, style="TFrame")
        self.canvas.create_window(400, 300, window=self.frame)

        welcome_label = ttk.Label(self.frame, text="DijkstraDrawer", style="TLabel", font=("Monaco", 60))
        welcome_label.pack(pady=20, padx=20)

        pharaf_label = ttk.Label(self.frame, text="Graficador de Nodos con el algoritmo Dijkstra", style="TLabel", font=("Serif", 20))
        pharaf_label.pack(pady=10, padx=20)

        start_button = ttk.Button(self.frame, text="Comenzar", style="TButton", command=start_callback)
        start_button.pack(pady=20)

