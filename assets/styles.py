from tkinter import ttk
from PIL import Image, ImageTk

def apply_styles():
    style = ttk.Style()

    style.configure("TButton",
                    padding=6,
                    relief="flat",
                    background="#ccc",
                    foreground="#333",
                    font=("Arial", 10))

    style.map("TButton",
              background=[('active', '#b5b5b5')],
              foreground=[('active', '#000')])

    style.configure("TFrame",
                    background="#f0f0f0")

    style.configure("TLabel",
                    background="#f0f0f0",
                    font=("Arial", 12))

    style.configure("TCanvas",
                    background="white",
                    borderwidth=0,
                    highlightthickness=0)

def set_canvas_background(canvas, image_path):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    
    canvas.create_image(0, 0, image=bg_image_tk, anchor='nw')
    
    canvas.image = bg_image_tk
