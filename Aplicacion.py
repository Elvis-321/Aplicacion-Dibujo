import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageDraw, ImageTk

# Variables globales para la imagen y el dibujo
image = None
draw = None
canvas_image = None

# Pilas para deshacer y rehacer
undo_stack = []
redo_stack = []

# Función para importar una imagen
def import_image():
    global image, draw, canvas_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        image = Image.open(file_path)
        
        # Mantener la relación de aspecto
        max_size = 500
        aspect_ratio = image.width / image.height
        if aspect_ratio > 1:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        draw = ImageDraw.Draw(image)
        canvas_image = ImageTk.PhotoImage(image)
        canvas.config(image=canvas_image)
        show_main_interface()

# Función para actualizar la imagen en el lienzo
def update_canvas():
    global canvas_image
    canvas_image = ImageTk.PhotoImage(image)
    canvas.config(image=canvas_image)

# Función para manejar el clic en la hoja de dibujo
def on_canvas_click(event):
    global selected_shape
    if selected_shape:
        x, y = event.x, event.y
        size = size_var.get()
        x1, y1 = x - size, y - size
        x2, y2 = x + size, y + size

        # Guardar el estado actual para la función deshacer
        undo_stack.append(image.copy())
        redo_stack.clear()

        if selected_shape == "circle":
            draw.ellipse([x1, y1, x2, y2], outline=pen_color, width=2)
        elif selected_shape == "square":
            draw.rectangle([x1, y1, x2, y2], outline=pen_color, width=2)
        elif selected_shape == "triangle":
            draw.polygon([x, y-size, x-size, y+size, x+size, y+size], outline=pen_color, width=2)
        elif selected_shape == "star":
            points = [
                (x, y-size),
                (x+size/3, y-size/3),
                (x+size, y-size/3),
                (x+size/2, y+size/3),
                (x+size/2, y+size),
                (x, y+size/2),
                (x-size/2, y+size),
                (x-size/2, y+size/3),
                (x-size, y-size/3),
                (x-size/3, y-size/3)
            ]
            draw.polygon(points, outline=pen_color, width=2)
        elif selected_shape == "hexagon":
            points = [
                (x, y-size),
                (x+size/2, y-size/2),
                (x+size/2, y+size/2),
                (x, y+size),
                (x-size/2, y+size/2),
                (x-size/2, y-size/2)
            ]
            draw.polygon(points, outline=pen_color, width=2)

        update_canvas()

# Función para deshacer la última acción
def undo():
    if undo_stack:
        redo_stack.append(image.copy())
        last_image = undo_stack.pop()
        restore_image(last_image)

# Función para rehacer la última acción deshecha
def redo():
    if redo_stack:
        undo_stack.append(image.copy())
        last_image = redo_stack.pop()
        restore_image(last_image)

# Función para restaurar la imagen a un estado anterior
def restore_image(pil_image):
    global image, draw, canvas_image
    image = pil_image
    draw = ImageDraw.Draw(image)
    update_canvas()

# Función para guardar la imagen
def save_image():
    global image
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Image", "*.png")])
    if file_path:
        image.save(file_path)

# Función para seleccionar una figura
def select_shape(shape):
    global selected_shape
    selected_shape = shape

# Función para cambiar el color de las figuras
def change_color(color):
    global pen_color
    pen_color = color

# Función para mostrar la interfaz principal
def show_main_interface():
    import_frame.pack_forget()
    menu_frame.pack(side=tk.TOP, fill=tk.X)
    canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    color_palette_frame.pack(side=tk.RIGHT, fill=tk.Y)
    size_frame.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Dibujar figuras")

# Configurar el tamaño de la ventana
root.geometry("900x600")

# Crear un marco para la importación de la imagen
import_frame = tk.Frame(root)
import_frame.pack(fill=tk.BOTH, expand=True)

# Botón para importar la imagen
import_button = tk.Button(import_frame, text="Importar Imagen", command=import_image)
import_button.pack(pady=20)

# Crear un marco para el menú superior
menu_frame = tk.Frame(root, bg="lightgray")

# Crear un marco para la hoja de dibujo y la paleta de colores
canvas_frame = tk.Frame(root)

# Crear un marco para la paleta de colores
color_palette_frame = tk.Frame(root, bg="lightgray", width=150)

# Crear un marco para el ajuste del tamaño de la figura
size_frame = tk.Frame(root, bg="lightgray")

# Crear el lienzo para mostrar la hoja de dibujo
canvas = tk.Label(canvas_frame)

# Crear los botones para las figuras geométricas en el menú superior
shapes = [("Círculo", "circle"), ("Cuadrado", "square"), ("Triángulo", "triangle"),
          ("Estrella", "star"), ("Hexágono", "hexagon")]
for (text, shape) in shapes:
    button = tk.Button(menu_frame, text=text, command=lambda s=shape: select_shape(s))
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Crear los botones para la paleta de colores
colors = ["black", "red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta"]
for color in colors:
    button = tk.Button(color_palette_frame, bg=color, width=10, height=2, command=lambda c=color: change_color(c))
    button.pack(pady=5)

# Agregar un botón para guardar la imagen
save_button = tk.Button(size_frame, text="Guardar Imagen", command=save_image)
save_button.pack(pady=10)

# Agregar una etiqueta y una barra deslizante para ajustar el tamaño de la figura
size_label = tk.Label(size_frame, text="Tamaño de Figura:")
size_label.pack(pady=5)

size_var = tk.IntVar(value=20)
size_slider = tk.Scale(size_frame, from_=10, to_=100, orient=tk.HORIZONTAL, variable=size_var)
size_slider.pack(pady=5)

# Establecer color inicial
pen_color = "black"
selected_shape = None

# Asociar el evento de clic en el lienzo con la función on_canvas_click
canvas.bind("<Button-1>", on_canvas_click)

# Asociar las teclas Ctrl+Z y Ctrl+Y para deshacer y rehacer
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())

# Ejecutar la aplicación
root.mainloop()
