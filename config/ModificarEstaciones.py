"""
Módulo para la gestión de estaciones del simulador de trenes.
Permite añadir, eliminar y actualizar estaciones en el sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ventana import SimuladorTrenes

from models.clases import Estacion


# Constantes de configuración
COORD_MIN = 0
COORD_MAX = 500


def gestionar_estaciones(simulador: 'SimuladorTrenes'):
    """
    Abre una ventana modal para gestionar estaciones.
    
    Args:
        simulador: Instancia del SimuladorTrenes
    """
    estaciones_window = tk.Toplevel(simulador.master)
    estaciones_window.title("Gestionar Estaciones")
    estaciones_window.geometry("500x600")
    estaciones_window.transient(simulador.master)
    estaciones_window.grab_set()

    # Panel de adición
    _crear_panel_añadir_estacion(estaciones_window, simulador)
    
    # Panel de eliminación
    station_listbox = _crear_panel_quitar_estacion(estaciones_window, simulador)
    
    # Cargar datos iniciales
    actualizar_estaciones(simulador, station_listbox)


def _crear_panel_añadir_estacion(parent: tk.Toplevel, simulador: 'SimuladorTrenes'):
    """
    Crea el panel para añadir nuevas estaciones.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
    """
    añadir_frame = ttk.LabelFrame(parent, text="Añadir Nueva Estación", padding=10)
    añadir_frame.pack(padx=10, pady=10, fill='x')
    
    # Campo: Nombre
    ttk.Label(añadir_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    nombre_entrada = ttk.Entry(añadir_frame, width=30)
    nombre_entrada.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Coordenada X
    ttk.Label(añadir_frame, text=f"Coord. X ({COORD_MIN}-{COORD_MAX}):").grid(
        row=1, column=0, padx=5, pady=5, sticky='e'
    )
    x_entry = ttk.Entry(añadir_frame, width=30)
    x_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Coordenada Y
    ttk.Label(añadir_frame, text=f"Coord. Y ({COORD_MIN}-{COORD_MAX}):").grid(
        row=2, column=0, padx=5, pady=5, sticky='e'
    )
    y_entry = ttk.Entry(añadir_frame, width=30)
    y_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    
    # Botón de añadir
    def handler_añadir():
        añadir_estacion(simulador, nombre_entrada, x_entry, y_entry)
    
    ttk.Button(
        añadir_frame,
        text="Añadir Estación",
        command=handler_añadir
    ).grid(row=3, column=0, columnspan=2, pady=10)


def _crear_panel_quitar_estacion(parent: tk.Toplevel, simulador: 'SimuladorTrenes') -> tk.Listbox:
    """
    Crea el panel para eliminar estaciones existentes.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
        
    Returns:
        Listbox con las estaciones
    """
    quitar_frame = ttk.LabelFrame(parent, text="Quitar Estación Existente", padding=10)
    quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Listbox con scrollbar
    list_container = ttk.Frame(quitar_frame)
    list_container.pack(fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(list_container, orient='vertical')
    station_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
    scrollbar.config(command=station_listbox.yview)
    
    station_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Botón de eliminar
    def handler_quitar():
        quitar_estacion(simulador, station_listbox)
    
    ttk.Button(
        quitar_frame,
        text="Quitar Estación Seleccionada",
        command=handler_quitar
    ).pack(pady=5)
    
    return station_listbox


def añadir_estacion(
    simulador: 'SimuladorTrenes',
    nombre_entrada: ttk.Entry,
    x_entry: ttk.Entry,
    y_entry: ttk.Entry
):
    """
    Añade una nueva estación al sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        nombre_entrada: Campo de entrada del nombre
        x_entry: Campo de entrada de coordenada X
        y_entry: Campo de entrada de coordenada Y
    """
    nombre = nombre_entrada.get().strip()
    
    # Validar nombre
    if not nombre:
        messagebox.showerror("Error", "Debe ingresar un nombre para la estación.")
        return
    
    if nombre in simulador.estaciones:
        messagebox.showerror("Error", f"La estación '{nombre}' ya existe.")
        return
    
    # Validar y obtener coordenadas
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Las coordenadas deben ser números enteros.")
        return
    
    # Validar rango de coordenadas
    if not (COORD_MIN <= x <= COORD_MAX and COORD_MIN <= y <= COORD_MAX):
        messagebox.showerror(
            "Error",
            f"Las coordenadas deben estar entre {COORD_MIN} y {COORD_MAX}."
        )
        return
    
    # Crear y añadir la estación
    try:
        nueva_estacion = Estacion(nombre, x, y)
        simulador.estaciones[nombre] = nueva_estacion
        
        # Actualizar interfaz
        simulador.dibujar_mapa()
        
        # Limpiar campos
        nombre_entrada.delete(0, tk.END)
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"Estación '{nombre}' añadida en ({x}, {y}).")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear la estación: {str(e)}")


def quitar_estacion(simulador: 'SimuladorTrenes', station_listbox: tk.Listbox):
    """
    Elimina una estación seleccionada y todas sus rutas asociadas.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        station_listbox: Listbox con las estaciones
    """
    seleccion = station_listbox.curselection()
    
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una estación para eliminar.")
        return
    
    # Obtener el nombre de la estación (solo la primera parte antes del paréntesis)
    texto_seleccionado = station_listbox.get(seleccion[0])
    nombre_estacion = texto_seleccionado.split(' (')[0]
    
    # Confirmar eliminación
    confirmacion = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Está seguro de eliminar la estación '{nombre_estacion}'?\n\n"
        f"Esto también eliminará todas las rutas asociadas a esta estación."
    )
    
    if not confirmacion:
        return
    
    try:
        # Eliminar la estación
        del simulador.estaciones[nombre_estacion]
        
        # Eliminar todas las rutas que incluyan esta estación
        rutas_originales = len(simulador.rutas)
        simulador.rutas = [
            ruta for ruta in simulador.rutas
            if ruta.origen != nombre_estacion and ruta.destino != nombre_estacion
        ]
        rutas_eliminadas = rutas_originales - len(simulador.rutas)
        
        # Actualizar interfaz
        actualizar_estaciones(simulador, station_listbox)
        simulador.dibujar_mapa()
        
        mensaje = f"Estación '{nombre_estacion}' eliminada correctamente."
        if rutas_eliminadas > 0:
            mensaje += f"\n{rutas_eliminadas} ruta(s) asociada(s) también eliminada(s)."
        
        messagebox.showinfo("Éxito", mensaje)
        
    except KeyError:
        messagebox.showerror("Error", f"La estación '{nombre_estacion}' no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar la estación: {str(e)}")


def actualizar_estaciones(simulador: 'SimuladorTrenes', listbox: tk.Listbox):
    """
    Actualiza el listbox con las estaciones actuales del sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        listbox: Listbox a actualizar
    """
    listbox.delete(0, tk.END)
    
    # Ordenar estaciones alfabéticamente para mejor visualización
    estaciones_ordenadas = sorted(simulador.estaciones.items())
    
    for nombre, estacion in estaciones_ordenadas:
        texto = f"{nombre} ({estacion.coordenada_x}, {estacion.coordenada_y})"
        listbox.insert(tk.END, texto)