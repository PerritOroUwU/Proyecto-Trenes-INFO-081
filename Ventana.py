import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
from typing import Dict, List, Optional

from logic.Guardado import guardar_datos, cargar_datos
from models.clases import Tren, Estacion, Ruta, Pasajero


class SimuladorTrenes:
    """Simulador de sistema ferroviario con gestión de trenes, estaciones y rutas."""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self._configurar_ventana()
        
        # Estructuras de datos principales
        self.trenes: Dict[str, Tren] = {}
        self.estaciones: Dict[str, Estacion] = {}
        self.rutas: List[Ruta] = []
        
        # Referencias a widgets
        self.trenes_listbox: Optional[tk.Listbox] = None
        self.map_canvas: Optional[tk.Canvas] = None
        self.main_content_frame: Optional[ttk.Frame] = None
        self.paneles: Dict[str, ttk.Frame] = {}
        
        self._inicializar_datos()
        self.crear_interfaz()

    def _configurar_ventana(self):
        """Configura las propiedades iniciales de la ventana principal."""
        self.master.title("Simulador de Trenes")
        self.master.geometry("800x600")
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    def _inicializar_datos(self):
        """Carga datos guardados o inicializa con valores por defecto."""
        data = cargar_datos()
        
        if not data["trenes"] and not data["estaciones"]:
            self._cargar_datos_default()
        else:
            self.trenes = self._deserializar_trenes(data["trenes"])
            self.estaciones = self._deserializar_estaciones(data["estaciones"])
            self.rutas = self._deserializar_rutas(data["rutas"])

    def _cargar_datos_default(self):
        """Carga los datos por defecto del sistema."""
        self.trenes = {
            "BMU": Tren(nombre="BMU", capacidad=236, combustible="Híbrido", velocidad_max=160),
            "EMU": Tren(nombre="EMU", capacidad=300, combustible="Eléctrico", velocidad_max=120)
        }
        
        self.estaciones = {
            "Estación Central": Estacion("Estación Central", 50, 200),
            "Rancagua": Estacion("Rancagua", 150, 300),
            "Talca": Estacion("Talca", 300, 100),
            "Chillán": Estacion("Chillán", 450, 400)
        }
        
        self.rutas = [
            Ruta("Estación Central", "Rancagua", 87),
            Ruta("Rancagua", "Talca", 200),
            Ruta("Talca", "Chillán", 180),
            Ruta("Estación Central", "Chillán", 254)
        ]

    # ========== MÉTODOS DE DESERIALIZACIÓN ==========
    
    def _deserializar_trenes(self, trenes_dict: dict) -> Dict[str, Tren]:
        """Convierte diccionarios JSON a objetos Tren."""
        return {
            nombre: Tren(
                nombre=nombre,
                capacidad=specs['capacidad'],
                combustible=specs['combustible'],
                velocidad_max=specs['velocidad_max']
            )
            for nombre, specs in trenes_dict.items()
        }

    def _deserializar_pasajero(self, pasajero_dict: dict) -> Pasajero:
        """Convierte un diccionario a objeto Pasajero."""
        tiempo_llegada = dt.datetime.fromisoformat(pasajero_dict["tiempo_llegada"])
        tiempo_partida = (
            dt.datetime.fromisoformat(pasajero_dict["tiempo_partida"])
            if pasajero_dict["tiempo_partida"] else None
        )
        
        pasajero = Pasajero(
            origen=pasajero_dict["origen"],
            destino=pasajero_dict["destino"],
            tiempo_llegada=tiempo_llegada
        )
        pasajero.id = pasajero_dict["id"]
        pasajero.tiempo_partida = tiempo_partida
        
        # Actualizar contador estático si es necesario
        if pasajero.id >= Pasajero.id_counter:
            Pasajero.id_counter = pasajero.id + 1
            
        return pasajero

    def _deserializar_estaciones(self, estaciones_dict: dict) -> Dict[str, Estacion]:
        """Convierte diccionarios JSON a objetos Estacion con sus pasajeros."""
        objetos_estacion = {}
        
        for nombre, specs in estaciones_dict.items():
            estacion = Estacion(
                nombre=nombre,
                coordenada_x=specs['coord_x'],
                coordenada_y=specs['coord_y']
            )
            
            # Reconstruir pasajeros si existen
            if specs.get("pasajeros_esperando"):
                for p_dict in specs["pasajeros_esperando"]:
                    pasajero = self._deserializar_pasajero(p_dict)
                    estacion.agregar_pasajero(pasajero)
            
            objetos_estacion[nombre] = estacion
            
        return objetos_estacion
    
    def _deserializar_rutas(self, rutas_lista: list) -> List[Ruta]:
        """Convierte lista de tuplas a objetos Ruta."""
        return [
            Ruta(origen=origen, destino=destino, distancia_km=distancia)
            for origen, destino, distancia in rutas_lista
        ]

    # ========== INTERFAZ PRINCIPAL ==========

    def crear_interfaz(self):
        """Crea la estructura completa de la interfaz."""
        self.crear_menu_lateral()
        
        self.main_content_frame = ttk.Frame(self.master)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1)

        self.crear_paneles_gestion()
        self.show_panel("mapa")

    def crear_menu_lateral(self):
        """Crea el menú lateral con botones de acción."""
        left_menu = ttk.Frame(self.master, padding="10")
        left_menu.grid(row=0, column=0, sticky="nsew")
        left_menu.grid_columnconfigure(0, weight=1)
        
        # Lista de botones con sus comandos
        botones = [
            ("Iniciar simulación", self.iniciar_simulacion),
            ("Ver Pasajeros a Bordo", self.mostrar_pasajeros_abordo)
            ("Acceder a datos de trenes", lambda: self.show_panel("trenes")),
            ("Acceder a datos de estación", lambda: self.show_panel("estaciones")),
            ("Acceder a datos de ruta", lambda: self.show_panel("rutas")),
            ("Modificar datos", self.modificar_datos),
            ("GUARDAR ESTADO", self.guardar_estado),
            ("CARGAR ESTADO", self.cargar_estado)

        ]
        
        # Crear cada botón
        for i, (text, command) in enumerate(botones):
            btn = ttk.Button(left_menu, text=text, command=command)
            btn.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
            
            # Debug: Imprimir cuando se crea cada botón
            print(f"Botón creado: '{text}' con comando: {command}")
        
        self.left_menu = left_menu

    def crear_paneles_gestion(self):
        """Crea todos los paneles de gestión y los coloca en el mismo espacio."""
        # Panel de mapa
        map_panel = self._crear_map_panel(self.main_content_frame)
        self.paneles["mapa"] = map_panel
        map_panel.grid(row=0, column=0, sticky="nsew")

        # Panel de trenes
        tren_panel = self._gestionar_trenes_ui(self.main_content_frame)
        self.paneles["trenes"] = tren_panel
        tren_panel.grid(row=0, column=0, sticky="nsew")
        
        # Panel de estaciones
        estacion_panel = self._gestionar_estaciones_ui(self.main_content_frame)
        self.paneles["estaciones"] = estacion_panel
        estacion_panel.grid(row=0, column=0, sticky="nsew")
        
        # Panel de rutas
        rutas_panel = self._gestionar_rutas_ui(self.main_content_frame)
        self.paneles["rutas"] = rutas_panel
        rutas_panel.grid(row=0, column=0, sticky="nsew")

    def show_panel(self, panel_name: str):
        """Muestra el panel solicitado y oculta los demás."""
        target_panel = self.paneles.get(panel_name)
        
        if not target_panel:
            print(f"Error: Panel '{panel_name}' no encontrado.")
            return

        # Ocultar todos los paneles
        for panel in self.paneles.values():
            panel.grid_remove()
            
        # Mostrar el panel solicitado
        target_panel.grid()

    # ========== PANEL DE TRENES ==========

    def _gestionar_trenes_ui(self, parent_frame: ttk.Frame) -> ttk.LabelFrame:
        """Crea el panel de gestión de trenes."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Trenes", padding=10)
        
        # Botón para añadir tren
        ttk.Button(
            panel,
            text="Añadir Nuevo Tren",
            command=self._agregar_y_actualizar_tren
        ).pack(pady=5, padx=10)
        
        # Sección para quitar trenes
        ttk.Label(panel, text="Quitar Tren Existente").pack(pady=5)
        
        self.trenes_listbox = tk.Listbox(panel, height=8)
        self.trenes_listbox.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(
            panel,
            text="Quitar Tren Seleccionado",
            command=self._quitar_y_actualizar_tren
        ).pack(pady=5)
        
        self._actualizar_listado_trenes()
        
        return panel

    def _actualizar_listado_trenes(self):
        """Recarga los nombres de los trenes en el Listbox."""
        if not hasattr(self, 'trenes_listbox') or self.trenes_listbox is None:
            return
        
        self.trenes_listbox.delete(0, tk.END)
        
        for nombre in self.trenes.keys():
            self.trenes_listbox.insert(tk.END, nombre)

    def _agregar_y_actualizar_tren(self):
        """Maneja la adición de un nuevo tren."""
        from config.ModificarTrenes import agregar_tren
        
        agregar_tren(self)
        self._actualizar_listado_trenes()

    def _quitar_y_actualizar_tren(self):
        """Maneja la eliminación de un tren seleccionado."""
        seleccion = self.trenes_listbox.curselection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un tren para quitar.")
            return

        nombre_tren = self.trenes_listbox.get(seleccion[0])
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de quitar el tren '{nombre_tren}'?"
        )
        
        if confirmacion:
            try:
                del self.trenes[nombre_tren]
                self._actualizar_listado_trenes()
                messagebox.showinfo("Éxito", f"Tren '{nombre_tren}' eliminado correctamente.")
            except KeyError:
                messagebox.showerror("Error", "El tren no se encontró en la base de datos.")

    # ========== PANEL DE ESTACIONES ==========

    def _gestionar_estaciones_ui(self, parent_frame: ttk.Frame) -> ttk.LabelFrame:
        """Crea el panel de gestión de estaciones."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Estaciones", padding=10)
        ttk.Label(panel, text="Interfaz de gestión de estaciones aquí").pack(padx=5, pady=5)
        return panel

    # ========== PANEL DE RUTAS ==========

    def _gestionar_rutas_ui(self, parent_frame: ttk.Frame) -> ttk.LabelFrame:
        """Crea el panel de gestión de rutas."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Rutas", padding=10)
        ttk.Label(panel, text="Interfaz de gestión de rutas aquí").pack(padx=5, pady=5)
        return panel

    # ========== PANEL DE MAPA ==========

    def _crear_map_panel(self, parent_frame: ttk.Frame) -> ttk.LabelFrame:
        """Crea el panel del mapa con canvas y scrollbars."""
        map_panel = ttk.LabelFrame(parent_frame, text="Rutas y Mapa", padding=5)
        map_panel.grid_columnconfigure(0, weight=1)
        map_panel.grid_rowconfigure(0, weight=1)
        
        map_container = ttk.Frame(map_panel)
        map_container.grid(row=0, column=0, sticky="nsew")
        map_container.grid_rowconfigure(0, weight=1)
        map_container.grid_columnconfigure(0, weight=1)
        
        # Crear scrollbars
        v_scrollbar = ttk.Scrollbar(map_container, orient="vertical")
        h_scrollbar = ttk.Scrollbar(map_container, orient="horizontal")

        # Crear canvas
        self.map_canvas = tk.Canvas(
            map_container,
            bg="white",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configurar scrollbars
        v_scrollbar.config(command=self.map_canvas.yview)
        h_scrollbar.config(command=self.map_canvas.xview)
        
        # Colocar elementos
        self.map_canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.dibujar_mapa()
        
        return map_panel

    def dibujar_mapa(self):
        """Dibuja las estaciones y rutas en el canvas."""
        if not self.map_canvas:
            return
            
        self.map_canvas.delete("all")
        
        RADIO_ESTACION = 5
        coordenadas = []
        
        # Dibujar rutas (líneas entre estaciones)
        for ruta in self.rutas:
            if ruta.origen in self.estaciones and ruta.destino in self.estaciones:
                est_origen = self.estaciones[ruta.origen]
                est_destino = self.estaciones[ruta.destino]
                
                self.map_canvas.create_line(
                    est_origen.coordenada_x, est_origen.coordenada_y,
                    est_destino.coordenada_x, est_destino.coordenada_y,
                    dash=(4, 2), width=2, fill="gray"
                )
        
        # Dibujar estaciones
        for nombre, estacion in self.estaciones.items():
            x, y = estacion.coordenada_x, estacion.coordenada_y
            
            # Círculo de la estación
            self.map_canvas.create_oval(
                x - RADIO_ESTACION, y - RADIO_ESTACION,
                x + RADIO_ESTACION, y + RADIO_ESTACION,
                fill="blue", outline="black"
            )
            
            # Etiqueta de la estación
            self.map_canvas.create_text(
                x, y - 15,
                text=nombre,
                anchor=tk.S,
                fill="black"
            )
            
            coordenadas.extend([x, y])
        
        # Configurar scrollregion
        if coordenadas:
            min_x = min(coordenadas[::2]) - 50
            min_y = min(coordenadas[1::2]) - 50
            max_x = max(coordenadas[::2]) + 50
            max_y = max(coordenadas[1::2]) + 50
        else:
            min_x, min_y, max_x, max_y = 0, 0, 500, 500
        
        self.map_canvas.config(scrollregion=(min_x, min_y, max_x, max_y))

    # ========== ACCIONES DEL MENÚ ==========

    def iniciar_simulacion(self):
        """Inicia la simulación del sistema ferroviario."""
        if not self.trenes or not self.estaciones:
            messagebox.showwarning(
                "Error de Simulación",
                "Debe tener al menos un tren y una estación para iniciar."
            )
            return
        
        self.generar_pasajeros_estaciones()
        self.actualizar_pasajeros()

        mensaje = (
            f"Simulación de Trenes Iniciada.\n\n"
            f"Parámetros cargados:\n"
            f"- Tipos de trenes: {len(self.trenes)}\n"
            f"- Estaciones: {len(self.estaciones)}\n"
            f"- Rutas definidas: {len(self.rutas)}\n\n"
            f"El motor de simulación está calculando los trayectos..."
        )
        messagebox.showinfo("Simulación en Curso", mensaje)
    
        # ========== GENERA PASAJEROS  ==========
    def generar_pasajeros_estaciones(self):
        """Genera pasajeros aleatorios en cada estación."""
        import random
        from models.clases import Pasajero
    
        for estacion in self.estaciones.values():
            num_pasajeros = random.randint(0, 3)  # máximo 3 pasajeros por estación por turno
            for _ in range(num_pasajeros):
                origen = estacion.nombre
                destino = random.choice([e for e in self.estaciones.keys() if e != origen])
                pasajero = Pasajero(origen, destino, dt.datetime.now())
                estacion.agregar_pasajero(pasajero)

    def actualizar_pasajeros(self):
        """Hace que los pasajeros suban y bajen del tren."""
        for tren in self.trenes.values():
            # Bajar pasajeros en la estación actual
            pasajeros_a_bajar = [p for p in getattr(tren, "pasajeros", []) if p.destino == getattr(tren, "ubicacion", None)]
            for p in pasajeros_a_bajar:
                tren.pasajeros.remove(p)
                if tren.ubicacion in self.estaciones:
                    self.estaciones[tren.ubicacion].agregar_pasajero(p)

        # Subir pasajeros desde la estación actual
            estacion = self.estaciones.get(getattr(tren, "ubicacion", None))
            if estacion:
                while estacion.pasajeros_esperando and len(getattr(tren, "pasajeros", [])) < tren.capacidad:
                    pasajero = estacion.pasajeros_esperando.pop(0)
                    tren.pasajeros.append(pasajero)

    def mostrar_pasajeros_abordo(self):
        """Muestra cuántos pasajeros hay en cada tren."""
        mensaje = ""
        for nombre, tren in self.trenes.items():
            cantidad = len(getattr(tren, "pasajeros", []))
            mensaje += f"{nombre}: {cantidad} pasajeros a bordo\n"
        messagebox.showinfo("Pasajeros a Bordo", mensaje)
    

    def modificar_datos(self):
        """Abre el módulo de modificación de datos."""
        print("DEBUG: modificar_datos() fue llamado")  # Debug
        
        # Versión alternativa: crear la ventana directamente aquí
        try:
            # Primero intentamos importar el módulo externo
            from config.ModificarDatos import modificar_datos
            print("DEBUG: Importación exitosa")  # Debug
            modificar_datos(self)
            print("DEBUG: Función modificar_datos ejecutada")  # Debug
        except ImportError as e:
            print(f"DEBUG: Error de importación - {e}")  # Debug
            # Si falla, creamos la ventana directamente
            self._crear_ventana_modificar_datos_directa()
        except Exception as e:
            print(f"DEBUG: Error general - {e}")  # Debug
            messagebox.showerror(
                "Error",
                f"Error al abrir la ventana de modificación:\n\n{str(e)}"
            )
    
    def _crear_ventana_modificar_datos_directa(self):
        """Crea la ventana de modificación de datos directamente (fallback)."""
        ventana_modificar = tk.Toplevel(self.master)
        ventana_modificar.title("Modificar Datos del Sistema")
        ventana_modificar.geometry("400x300")
        ventana_modificar.transient(self.master)
        ventana_modificar.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(ventana_modificar, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Seleccione qué desea modificar:",
            font=('TkDefaultFont', 11, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill='both', expand=True)
        botones_frame.grid_columnconfigure(0, weight=1)
        
        # Botón Modificar Trenes
        ttk.Button(
            botones_frame,
            text="Modificar Trenes",
            command=lambda: self._abrir_gestionar_trenes(ventana_modificar),
            width=30
        ).grid(row=0, column=0, pady=10, padx=20)
        
        # Botón Modificar Estaciones
        ttk.Button(
            botones_frame,
            text="Modificar Estaciones",
            command=lambda: self._abrir_gestionar_estaciones(ventana_modificar),
            width=30
        ).grid(row=1, column=0, pady=10, padx=20)
        
        # Botón Modificar Rutas
        ttk.Button(
            botones_frame,
            text="Modificar Rutas",
            command=lambda: self._abrir_gestionar_rutas(ventana_modificar),
            width=30
        ).grid(row=2, column=0, pady=10, padx=20)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Botón cerrar
        ttk.Button(
            main_frame,
            text="Cerrar",
            command=ventana_modificar.destroy,
            width=15
        ).pack(pady=(0, 10))
        
        # Centrar ventana
        ventana_modificar.update_idletasks()
        x = (ventana_modificar.winfo_screenwidth() // 2) - (ventana_modificar.winfo_width() // 2)
        y = (ventana_modificar.winfo_screenheight() // 2) - (ventana_modificar.winfo_height() // 2)
        ventana_modificar.geometry(f"+{x}+{y}")
    
    def _abrir_gestionar_trenes(self, parent_window=None):
        """Abre la ventana de gestión de trenes."""
        try:
            from config.ModificarTrenes import gestionar_trenes
            gestionar_trenes(self)
        except ImportError:
            messagebox.showerror(
                "Error",
                "No se encontró el módulo ModificarTrenes.py en la carpeta config/"
            )
    
    def _abrir_gestionar_estaciones(self, parent_window=None):
        """Abre la ventana de gestión de estaciones."""
        try:
            from config.ModificarEstaciones import gestionar_estaciones
            gestionar_estaciones(self)
        except ImportError:
            messagebox.showerror(
                "Error",
                "No se encontró el módulo ModificarEstaciones.py en la carpeta config/"
            )
    
    def _abrir_gestionar_rutas(self, parent_window=None):
        """Abre la ventana de gestión de rutas."""
        try:
            from config.ModificarRutas import gestionar_rutas
            gestionar_rutas(self)
        except ImportError:
            messagebox.showerror(
                "Error",
                "No se encontró el módulo ModificarRutas.py en la carpeta config/"
            )
    
    def guardar_cambios(self):
        """Guarda todos los cambios realizados en el sistema."""
        self.guardar_estado()
        if hasattr(self, '_actualizar_listado_trenes'):
            self._actualizar_listado_trenes()
        self.dibujar_mapa()

    def guardar_estado(self):
        """Guarda el estado actual del simulador."""
        if guardar_datos(self.trenes, self.estaciones, self.rutas):
            messagebox.showinfo("Guardado", "El estado ha sido guardado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar el archivo de datos.")

    def cargar_estado(self):
        """Carga un estado previamente guardado."""
        data = cargar_datos()
        
        if data["trenes"] or data["estaciones"]:
            self.trenes = self._deserializar_trenes(data["trenes"])
            self.estaciones = self._deserializar_estaciones(data["estaciones"])
            self.rutas = self._deserializar_rutas(data["rutas"])
            
            self._actualizar_listado_trenes()
            self.dibujar_mapa()
            
            messagebox.showinfo("Cargado", "El estado ha sido cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay datos guardados para cargar.")


def main():
    """Punto de entrada de la aplicación."""
    root = tk.Tk()
    app = SimuladorTrenes(root)
    root.mainloop()


if __name__ == '__main__':
    main()