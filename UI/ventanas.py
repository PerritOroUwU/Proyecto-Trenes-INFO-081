import tkinter as tk

root = tk.Tk()

def acción_de_boton():
        ventana = tk.Toplevel(root)
        ventana.geometry("1024x600")
        ventana.title("Simulación Iniciada")
        etiqueta = tk.Label(
            ventana,
            text="Simulación en curso...",
            font=("Arial", 24)
        )
        etiqueta.pack(pady=20)
