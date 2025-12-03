"""
Módulo para la gestión de trenes del simulador.
Permite añadir, eliminar y actualizar tipos de trenes en el sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ventana import SimuladorTrenes

from models.clases import Tren


# Constantes de configuración
COMBUSTIBLES_DISPONIBLES = ["Diésel", "Eléctrico", "Híbrido", "Otro"]
CAPACIDAD_MIN = 1
VELOCIDAD_MIN = 1


def gestionar_trenes(simulador: 'SimuladorTrenes'):
    """
    Abre una ventana modal para gestionar tipos de trenes.
    
    Args:
        simulador: Instancia del SimuladorTrenes
    """
    ventana_trenes = tk.Toplevel(simulador.master)
    ventana_trenes.title("Gestionar Tipos de Trenes")
    ventana_trenes.geometry("550x600")
    ventana_trenes.transient(simulador.master)
    ventana_trenes.grab_set()

    # Panel de adición
    _crear_panel_añadir_tren(ventana_trenes, simulador)
    
    # Panel de eliminación
    lista_trenes = _crear_panel_quitar_tren(ventana_trenes, simulador)
    
    # Cargar datos iniciales
    actualizar_trenes(simulador, lista_trenes)


def _crear_panel_añadir_tren(parent: tk.Toplevel, simulador: 'SimuladorTrenes'):
    """
    Crea el panel para añadir nuevos tipos de trenes.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
    """
    añadir_frame = ttk.LabelFrame(parent, text="Añadir Nuevo Tren", padding=10)
    añadir_frame.pack(padx=10, pady=10, fill='x')
    
    # Campo: Nombre/Tipo
    ttk.Label(añadir_frame, text="Nombre/Tipo:").grid(
        row=0, column=0, padx=5, pady=5, sticky='e'
    )
    nombre_entrada = ttk.Entry(añadir_frame, width=25)
    nombre_entrada.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Capacidad
    ttk.Label(añadir_frame, text="Capacidad (Pax):").grid(
        row=1, column=0, padx=5, pady=5, sticky='e'
    )
    entrada_capacidad = ttk.Entry(añadir_frame, width=25)
    entrada_capacidad.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Velocidad Máxima
    ttk.Label(añadir_frame, text="Vel. Máx (km/h):").grid(
        row=2, column=0, padx=5, pady=5, sticky='e'
    )
    entrada_velocidad = ttk.Entry(añadir_frame, width=25)
    entrada_velocidad.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Combustible
    ttk.Label(añadir_frame, text="Combustible:").grid(
        row=3, column=0, padx=5, pady=5, sticky='e'
    )
    combustible_cb = ttk.Combobox(
        añadir_frame,
        values=COMBUSTIBLES_DISPONIBLES,
        state='readonly',
        width=23
    )
    combustible_cb.set(COMBUSTIBLES_DISPONIBLES[0])
    combustible_cb.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    
    # Botón de añadir
    def handler_agregar():
        agregar_tren(simulador, nombre_entrada, entrada_capacidad, 
                     entrada_velocidad, combustible_cb)
    
    ttk.Button(
        añadir_frame,
        text="Añadir Tren",
        command=handler_agregar
    ).grid(row=4, column=0, columnspan=2, pady=10)


def _crear_panel_quitar_tren(parent: tk.Toplevel, simulador: 'SimuladorTrenes') -> tk.Listbox:
    """
    Crea el panel para eliminar trenes existentes.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
        
    Returns:
        Listbox con los trenes
    """
    quitar_frame = ttk.LabelFrame(parent, text="Quitar Tren Existente", padding=10)
    quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Listbox con scrollbar
    list_container = ttk.Frame(quitar_frame)
    list_container.pack(fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(list_container, orient='vertical')
    lista_trenes = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_trenes.yview)
    
    lista_trenes.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    scrollbar.pack(side='right', fill='y')

    # Botón de eliminar
    def handler_quitar():
        quitar_tren(simulador, lista_trenes)
    
    ttk.Button(
        quitar_frame,
        text="Quitar Tren Seleccionado",
        command=handler_quitar
    ).pack(pady=5)
    
    return lista_trenes


def agregar_tren(
    simulador: 'SimuladorTrenes',
    nombre_entrada: ttk.Entry,
    entrada_capacidad: ttk.Entry,
    entrada_velocidad: ttk.Entry,
    combustible_cb: ttk.Combobox
):
    """
    Añade un nuevo tipo de tren al sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        nombre_entrada: Campo de entrada del nombre
        entrada_capacidad: Campo de entrada de capacidad
        entrada_velocidad: Campo de entrada de velocidad máxima
        combustible_cb: Combobox de selección de combustible
    """
    nombre = nombre_entrada.get().strip().upper()
    combustible = combustible_cb.get()
    
    # Validar nombre
    if not nombre:
        messagebox.showerror("Error", "Debe ingresar un nombre para el tren.")
        return
    
    if nombre in simulador.trenes:
        messagebox.showerror("Error", f"El tren '{nombre}' ya existe.")
        return
    
    # Validar y obtener capacidad
    try:
        capacidad = int(entrada_capacidad.get())
    except ValueError:
        messagebox.showerror("Error", "La capacidad debe ser un número entero.")
        return
    
    if capacidad < CAPACIDAD_MIN:
        messagebox.showerror(
            "Error",
            f"La capacidad debe ser mayor o igual a {CAPACIDAD_MIN}."
        )
        return
    
    # Validar y obtener velocidad
    try:
        velocidad = int(entrada_velocidad.get())
    except ValueError:
        messagebox.showerror("Error", "La velocidad máxima debe ser un número entero.")
        return
    
    if velocidad < VELOCIDAD_MIN:
        messagebox.showerror(
            "Error",
            f"La velocidad máxima debe ser mayor o igual a {VELOCIDAD_MIN} km/h."
        )
        return
    
    # Crear y añadir el tren
    try:
        nuevo_tren = Tren(
            nombre=nombre,
            capacidad=capacidad,
            combustible=combustible,
            velocidad_max=velocidad
        )
        simulador.trenes[nombre] = nuevo_tren
        
        # Actualizar interfaz si existe el listbox en el panel principal
        if hasattr(simulador, '_actualizar_listado_trenes'):
            simulador._actualizar_listado_trenes()
        
        # Limpiar campos
        nombre_entrada.delete(0, tk.END)
        entrada_capacidad.delete(0, tk.END)
        entrada_velocidad.delete(0, tk.END)
        combustible_cb.set(COMBUSTIBLES_DISPONIBLES[0])
        
        messagebox.showinfo(
            "Éxito",
            f"Tren '{nombre}' añadido correctamente.\n\n"
            f"Especificaciones:\n"
            f"- Capacidad: {capacidad} pasajeros\n"
            f"- Combustible: {combustible}\n"
            f"- Velocidad máxima: {velocidad} km/h"
        )
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el tren: {str(e)}")


def quitar_tren(simulador: 'SimuladorTrenes', lista_trenes: tk.Listbox):
    """
    Elimina un tipo de tren seleccionado del sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        lista_trenes: Listbox con los trenes
    """
    seleccion = lista_trenes.curselection()
    
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar un tren para eliminar.")
        return
    
    # Obtener el nombre del tren (primera parte antes del paréntesis)
    texto_seleccionado = lista_trenes.get(seleccion[0])
    nombre_tren = texto_seleccionado.split(" (")[0]
    
    # Confirmar eliminación
    confirmacion = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Está seguro de eliminar el tren '{nombre_tren}'?\n\n"
        f"Esta acción no se puede deshacer."
    )
    
    if not confirmacion:
        return
    
    try:
        # Eliminar el tren
        del simulador.trenes[nombre_tren]
        
        # Actualizar listbox de la ventana modal
        actualizar_trenes(simulador, lista_trenes)
        
        # Actualizar interfaz principal si existe
        if hasattr(simulador, '_actualizar_listado_trenes'):
            simulador._actualizar_listado_trenes()
        
        messagebox.showinfo("Éxito", f"Tren '{nombre_tren}' eliminado correctamente.")
        
    except KeyError:
        messagebox.showerror("Error", f"No se encontró el tren '{nombre_tren}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar el tren: {str(e)}")


def actualizar_trenes(simulador: 'SimuladorTrenes', listbox: tk.Listbox):
    """
    Actualiza el listbox con los trenes actuales del sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        listbox: Listbox a actualizar
    """
    listbox.delete(0, tk.END)
    
    # Ordenar trenes alfabéticamente para mejor visualización
    trenes_ordenados = sorted(simulador.trenes.items())
    
    for nombre, tren in trenes_ordenados:
        # Acceder a los atributos del objeto Tren
        display_text = (
            f"{nombre} "
            f"(Cap: {tren.capacidad}, "
            f"Comb: {tren.combustible}, "
            f"Vel: {tren.velocidad_max} km/h)"
        )
        listbox.insert(tk.END, display_text)


# Función auxiliar para uso desde el panel principal
def agregar_tren_simple(simulador: 'SimuladorTrenes'):
    """
    Wrapper simplificado para abrir el diálogo de añadir tren.
    Se usa desde el panel principal de gestión de trenes.
    
    Args:
        simulador: Instancia del SimuladorTrenes
    """
    gestionar_trenes(simulador)