"""
Módulo principal para modificar datos del simulador de trenes.
Proporciona una ventana central con acceso a la gestión de trenes, estaciones y rutas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ventana import SimuladorTrenes


def modificar_datos(simulador: 'SimuladorTrenes'):
    """
    Abre una ventana central para acceder a las opciones de modificación de datos.
    
    Args:
        simulador: Instancia del SimuladorTrenes
    """
    print("DEBUG ModificarDatos: Iniciando creación de ventana")  # Debug
    
    try:
        ventana_modificar = tk.Toplevel(simulador.master)
        ventana_modificar.title("Modificar Datos del Sistema")
        ventana_modificar.geometry("450x350")
        
        print("DEBUG ModificarDatos: Ventana Toplevel creada")  # Debug
        
        # Hacer la ventana modal y traerla al frente
        ventana_modificar.transient(simulador.master)
        ventana_modificar.grab_set()
        ventana_modificar.lift()
        ventana_modificar.focus_force()
        
        # Asegurar que sea visible
        ventana_modificar.attributes('-topmost', True)
        ventana_modificar.after(100, lambda: ventana_modificar.attributes('-topmost', False))
        
        print("DEBUG ModificarDatos: Configuración modal aplicada")  # Debug
    
        # Frame principal con padding
        main_frame = ttk.Frame(ventana_modificar, padding=20)
        main_frame.pack(fill='both', expand=True)
    
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Seleccione qué desea modificar:",
            font=('TkDefaultFont', 11, 'bold')
        )
        titulo.pack(pady=(0, 20))
    
        # Frame para los botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill='both', expand=True)
    
        # Configurar grid del frame de botones
        botones_frame.grid_columnconfigure(0, weight=1)
    
        # Botón 1: Modificar Trenes
        btn_trenes = ttk.Button(
            botones_frame,
            text="Modificar Trenes",
            command=lambda: _abrir_gestion_trenes(simulador, ventana_modificar),
            width=30
        )
        btn_trenes.grid(row=0, column=0, pady=10, padx=20)
    
        # Botón 2: Modificar Estaciones
        btn_estaciones = ttk.Button(
            botones_frame,
            text="Modificar Estaciones",
            command=lambda: _abrir_gestion_estaciones(simulador, ventana_modificar),
            width=30
        )
        btn_estaciones.grid(row=1, column=0, pady=10, padx=20)
    
        # Botón 3: Modificar Rutas
        btn_rutas = ttk.Button(
            botones_frame,
            text="Modificar Rutas",
            command=lambda: _abrir_gestion_rutas(simulador, ventana_modificar),
            width=30
        )
        btn_rutas.grid(row=2, column=0, pady=10, padx=20)
    
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
    
        # Botón de cerrar
        btn_cerrar = ttk.Button(
            main_frame,
            text="Cerrar",
         command=ventana_modificar.destroy,
            width=15
        )
        btn_cerrar.pack(pady=(0, 10))
    
            # Centrar la ventana en la pantalla
        ventana_modificar.update_idletasks()
        ancho_ventana = ventana_modificar.winfo_width()
        alto_ventana = ventana_modificar.winfo_height()
        ancho_pantalla = ventana_modificar.winfo_screenwidth()
        alto_pantalla = ventana_modificar.winfo_screenheight()
        
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        
        ventana_modificar.geometry(f"450x350+{x}+{y}")
        
        print("DEBUG ModificarDatos: Ventana centrada")  # Debug
        print(f"DEBUG ModificarDatos: Geometría: {ventana_modificar.geometry()}")  # Debug
        print(f"DEBUG ModificarDatos: Ventana visible: {ventana_modificar.winfo_viewable()}")  # Debug
        
        # Forzar actualización
        ventana_modificar.update()
        
    except Exception as e:
        print(f"DEBUG ModificarDatos: ERROR - {e}")  # Debug
        messagebox.showerror("Error", f"Error al crear la ventana:\n{str(e)}")
        return


def _abrir_gestion_trenes(simulador: 'SimuladorTrenes', parent_window: tk.Toplevel):
    """
    Abre el módulo de gestión de trenes.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        parent_window: Ventana padre (puede ser None)
    """
    from config.ModificarTrenes import gestionar_trenes
    gestionar_trenes(simulador)


def _abrir_gestion_estaciones(simulador: 'SimuladorTrenes', parent_window: tk.Toplevel):
    """
    Abre el módulo de gestión de estaciones.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        parent_window: Ventana padre (puede ser None)
    """
    from config.ModificarEstaciones import gestionar_estaciones
    gestionar_estaciones(simulador)


def _abrir_gestion_rutas(simulador: 'SimuladorTrenes', parent_window: tk.Toplevel):
    """
    Abre el módulo de gestión de rutas.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        parent_window: Ventana padre (puede ser None)
    """
    from config.ModificarRutas import gestionar_rutas
    gestionar_rutas(simulador)