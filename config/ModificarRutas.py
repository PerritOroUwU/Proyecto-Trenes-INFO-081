"""
Módulo para la gestión de rutas del simulador de trenes.
Permite añadir, eliminar y actualizar rutas entre estaciones.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ventana import SimuladorTrenes

from models.clases import Ruta


# Constantes de configuración
DISTANCIA_MIN = 1


def gestionar_rutas(simulador: 'SimuladorTrenes'):
    """
    Abre una ventana modal para gestionar rutas entre estaciones.
    
    Args:
        simulador: Instancia del SimuladorTrenes
    """
    ventana_rutas = tk.Toplevel(simulador.master)
    ventana_rutas.title("Gestionar Rutas")
    ventana_rutas.geometry("550x600")
    ventana_rutas.transient(simulador.master)
    ventana_rutas.grab_set()

    # Panel de adición
    ruta_listbox = _crear_panel_añadir_ruta(ventana_rutas, simulador)
    
    # Panel de eliminación
    _crear_panel_quitar_ruta(ventana_rutas, simulador, ruta_listbox)
    
    # Cargar datos iniciales
    actualizar_rutas(simulador, ruta_listbox)


def _crear_panel_añadir_ruta(parent: tk.Toplevel, simulador: 'SimuladorTrenes') -> tk.Listbox:
    """
    Crea el panel para añadir nuevas rutas.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
        
    Returns:
        Listbox que será usado en el panel de eliminación
    """
    añadir_frame = ttk.LabelFrame(parent, text="Añadir Nueva Ruta", padding=10)
    añadir_frame.pack(padx=10, pady=10, fill='x')
    
    # Obtener nombres de estaciones ordenados
    estacion_nombres = sorted(simulador.estaciones.keys())
    
    if not estacion_nombres:
        ttk.Label(
            añadir_frame,
            text="No hay estaciones disponibles. Añada estaciones primero.",
            foreground="red"
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        
        # Crear listbox vacío y retornar
        ruta_listbox = tk.Listbox(parent)
        return ruta_listbox
    
    # Campo: Estación de Origen
    ttk.Label(añadir_frame, text="Origen:").grid(
        row=0, column=0, padx=5, pady=5, sticky='e'
    )
    origen_cb = ttk.Combobox(
        añadir_frame,
        values=estacion_nombres,
        state='readonly',
        width=23
    )
    origen_cb.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Estación de Destino
    ttk.Label(añadir_frame, text="Destino:").grid(
        row=1, column=0, padx=5, pady=5, sticky='e'
    )
    destino_cb = ttk.Combobox(
        añadir_frame,
        values=estacion_nombres,
        state='readonly',
        width=23
    )
    destino_cb.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    # Campo: Distancia
    ttk.Label(añadir_frame, text="Distancia (km):").grid(
        row=2, column=0, padx=5, pady=5, sticky='e'
    )
    entrada_distancia = ttk.Entry(añadir_frame, width=25)
    entrada_distancia.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    
    # Crear el listbox que se usará en el panel de eliminación
    quitar_frame = ttk.LabelFrame(parent, text="Quitar Ruta Existente", padding=10)
    quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)
    
    list_container = ttk.Frame(quitar_frame)
    list_container.pack(fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(list_container, orient='vertical')
    ruta_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
    scrollbar.config(command=ruta_listbox.yview)
    
    ruta_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    scrollbar.pack(side='right', fill='y')
    
    # Botón de añadir
    def handler_añadir():
        añadir_ruta(simulador, origen_cb, destino_cb, entrada_distancia, ruta_listbox)
    
    ttk.Button(
        añadir_frame,
        text="Añadir Ruta",
        command=handler_añadir
    ).grid(row=3, column=0, columnspan=2, pady=10)
    
    return ruta_listbox


def _crear_panel_quitar_ruta(
    parent: tk.Toplevel,
    simulador: 'SimuladorTrenes',
    ruta_listbox: tk.Listbox
):
    """
    Añade el botón de eliminación al panel de rutas.
    
    Args:
        parent: Ventana padre
        simulador: Instancia del SimuladorTrenes
        ruta_listbox: Listbox con las rutas
    """
    # El frame ya fue creado en _crear_panel_añadir_ruta
    # Solo necesitamos encontrarlo y añadir el botón
    for widget in parent.winfo_children():
        if isinstance(widget, ttk.LabelFrame) and widget.cget('text') == "Quitar Ruta Existente":
            def handler_quitar():
                quitar_ruta(simulador, ruta_listbox)
            
            ttk.Button(
                widget,
                text="Quitar Ruta Seleccionada",
                command=handler_quitar
            ).pack(pady=5)
            break


def añadir_ruta(
    simulador: 'SimuladorTrenes',
    origen_cb: ttk.Combobox,
    destino_cb: ttk.Combobox,
    entrada_distancia: ttk.Entry,
    ruta_listbox: tk.Listbox
):
    """
    Añade una nueva ruta entre dos estaciones.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        origen_cb: Combobox de selección de origen
        destino_cb: Combobox de selección de destino
        entrada_distancia: Campo de entrada de distancia
        ruta_listbox: Listbox para actualizar
    """
    origen = origen_cb.get()
    destino = destino_cb.get()
    
    # Validar selección de origen
    if not origen:
        messagebox.showerror("Error", "Debe seleccionar una estación de origen.")
        return
    
    # Validar selección de destino
    if not destino:
        messagebox.showerror("Error", "Debe seleccionar una estación de destino.")
        return
    
    # Validar que origen y destino sean diferentes
    if origen == destino:
        messagebox.showerror("Error", "El origen y destino deben ser diferentes.")
        return
    
    # Validar y obtener distancia
    try:
        distancia = int(entrada_distancia.get())
    except ValueError:
        messagebox.showerror("Error", "La distancia debe ser un número entero.")
        return
    
    if distancia < DISTANCIA_MIN:
        messagebox.showerror(
            "Error",
            f"La distancia debe ser mayor o igual a {DISTANCIA_MIN} km."
        )
        return
    
    # Verificar si la ruta ya existe (en cualquier dirección)
    if _ruta_existe(simulador, origen, destino, distancia):
        messagebox.showerror(
            "Error",
            f"La ruta entre '{origen}' y '{destino}' ya existe."
        )
        return
    
    # Crear y añadir la ruta
    try:
        nueva_ruta = Ruta(
            origen=origen,
            destino=destino,
            distancia_km=distancia
        )
        simulador.rutas.append(nueva_ruta)
        
        # Actualizar interfaz
        actualizar_rutas(simulador, ruta_listbox)
        simulador.dibujar_mapa()
        
        # Limpiar campos
        origen_cb.set('')
        destino_cb.set('')
        entrada_distancia.delete(0, tk.END)
        
        messagebox.showinfo(
            "Éxito",
            f"Ruta añadida correctamente:\n\n"
            f"{origen} → {destino}\n"
            f"Distancia: {distancia} km"
        )
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear la ruta: {str(e)}")


def quitar_ruta(simulador: 'SimuladorTrenes', ruta_listbox: tk.Listbox):
    """
    Elimina una ruta seleccionada del sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        ruta_listbox: Listbox con las rutas
    """
    seleccion = ruta_listbox.curselection()
    
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una ruta para eliminar.")
        return
    
    # Obtener el texto seleccionado y parsearlo
    texto_seleccionado = ruta_listbox.get(seleccion[0])
    
    try:
        # Parsear el formato: "Origen → Destino (distancia km)"
        partes = texto_seleccionado.split(" → ")
        origen = partes[0].strip()
        
        partes_destino = partes[1].split(" (")
        destino = partes_destino[0].strip()
        distancia = int(partes_destino[1].replace(" km)", "").strip())
        
    except (IndexError, ValueError) as e:
        messagebox.showerror("Error", "Error al procesar la ruta seleccionada.")
        return
    
    # Confirmar eliminación
    confirmacion = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Está seguro de eliminar la ruta?\n\n"
        f"{origen} → {destino}\n"
        f"Distancia: {distancia} km"
    )
    
    if not confirmacion:
        return
    
    try:
        # Buscar y eliminar la ruta
        ruta_eliminada = False
        
        for i, ruta in enumerate(simulador.rutas):
            if (ruta.origen == origen and 
                ruta.destino == destino and 
                ruta.distancia_km == distancia):
                del simulador.rutas[i]
                ruta_eliminada = True
                break
            # Verificar también en dirección inversa
            elif (ruta.origen == destino and 
                  ruta.destino == origen and 
                  ruta.distancia_km == distancia):
                del simulador.rutas[i]
                ruta_eliminada = True
                break
        
        if ruta_eliminada:
            # Actualizar interfaz
            actualizar_rutas(simulador, ruta_listbox)
            simulador.dibujar_mapa()
            
            messagebox.showinfo("Éxito", f"Ruta {origen} → {destino} eliminada correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró la ruta especificada.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar la ruta: {str(e)}")


def actualizar_rutas(simulador: 'SimuladorTrenes', listbox: tk.Listbox):
    """
    Actualiza el listbox con las rutas actuales del sistema.
    
    Args:
        simulador: Instancia del SimuladorTrenes
        listbox: Listbox a actualizar
    """
    listbox.delete(0, tk.END)
    
    # Ordenar rutas por origen y luego por destino
    rutas_ordenadas = sorted(
        simulador.rutas,
        key=lambda r: (r.origen, r.destino)
    )
    
    for ruta in rutas_ordenadas:
        display_text = f"{ruta.origen} → {ruta.destino} ({ruta.distancia_km} km)"
        listbox.insert(tk.END, display_text)


def _ruta_existe(
    simulador: 'SimuladorTrenes',
    origen: str,
    destino: str,
    distancia: int
) -> bool:
    """
    Verifica si una ruta ya existe en el sistema (en cualquier dirección).
    
    Args:
        simulador: Instancia del SimuladorTrenes
        origen: Estación de origen
        destino: Estación de destino
        distancia: Distancia en kilómetros
        
    Returns:
        True si la ruta existe, False en caso contrario
    """
    for ruta in simulador.rutas:
        # Verificar ruta directa
        if (ruta.origen == origen and 
            ruta.destino == destino and 
            ruta.distancia_km == distancia):
            return True
        # Verificar ruta inversa
        if (ruta.origen == destino and 
            ruta.destino == origen and 
            ruta.distancia_km == distancia):
            return True
    
    return False