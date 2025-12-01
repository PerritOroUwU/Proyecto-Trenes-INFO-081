import tkinter as tk
from Datos.rutas import rutas

def acción_de_boton():
    ventana = tk.Toplevel()
    ventana.title("Ventana generada por un botón")
    ventana.geometry("300x200")

    texto = tk.Label(ventana, text="Aquí irá otra información")
    texto.pack(pady=20)


# ventana que muestra las rutas
def ventana_rutas():
    rutas = RutasTren() 

    ventana = tk.Toplevel()
    ventana.title("Datos de rutas")
    ventana.geometry("350x400")

    titulo = tk.Label(ventana, text="Rutas disponibles", font=("Arial", 12))
    titulo.pack(pady=10)

    lista = tk.Listbox(ventana, width=40, height=15)
    lista.pack()

    for ruta in rutas.obtener_rutas():
        lista.insert(tk.END, ruta)


# Esta función es la que usará el botón
def acción_de_boton_rutas():
    ventana_rutas()
