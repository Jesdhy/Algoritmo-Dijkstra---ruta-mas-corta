import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets'))
from styles import apply_styles
from bienvenida import WelcomeScreen
from dijkstra import GraphApp

def start_app(root):
    root.destroy()
    root2 = tk.Tk()
    apply_styles()
    GraphApp(root2)
    root2.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    apply_styles()
    WelcomeScreen(root, lambda: start_app(root))
    root.mainloop()
