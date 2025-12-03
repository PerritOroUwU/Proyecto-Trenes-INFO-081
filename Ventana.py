import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
from logic.Guardado import guardar_datos, cargar_datos
from models.rutas import __init__
from models.clases import Tren, Estacion, Ruta, Pasajero
import datetime as dt

class SimuladorTrenes:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Trenes")        
        
        master.geometry("800x600")

        data = cargar_datos()

        default_trenes = {
            "BHU": Tren(nombre="BHU", capacidad=150, combustible="Diésel", velocidad_max=120),
            "EMU": Tren(nombre="EMU", capacidad=300, combustible="Eléctrico", velocidad_max=160),
            "C-2500": Tren(nombre="C-2500", capacidad=200, combustible="Híbrido", velocidad_max=140)
        }
        
        # 2. Definir Estaciones y Rutas por defecto (Asegúrate de usar la clase Estacion aquí también)
        default_estaciones = {
            "Santiago": Estacion("Santiago", 50, 200),
            "Rancagua": Estacion("Rancagua", 150, 300),
            "Talca": Estacion("Talca", 300, 100),
            "Chillán": Estacion("Chillán", 450, 400)
        }
        default_rutas = [ 
            Ruta("Santiago", "Rancagua", 80), 
            Ruta("Rancagua", "Talca", 150), 
            Ruta("Talca", "Chillán", 100) 
        ]
        # 3. Asignar los datos cargados o los valores por defecto
        
        # Si el archivo de guardado no existe o devuelve datos vacíos
        if not data["trenes"] and not data["estaciones"]:
            self.trenes = default_trenes
            self.estaciones = default_estaciones
            self.rutas = default_rutas
        else:
            # Aquí es donde ocurre el cambio crucial: deserializar los datos cargados
            self.trenes = self.deserializar_trenes(data["trenes"])
            self.estaciones = self.deserializar_estaciones(data["estaciones"])
            self.rutas = self.deserializar_rutas(data["rutas"]) 
            
        self.crear_interfaz()

    def gestionar_trenes_ui(self, parent_frame):
        """Panel de gestión de trenes (implementación básica)."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Trenes", padding=10)
        ttk.Label(panel, text="Interfaz de gestión de trenes aquí").pack(padx=5, pady=5)
        return panel

    def gestionar_estaciones_ui(self, parent_frame):
        """Panel de gestión de estaciones (implementación básica)."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Estaciones", padding=10)
        ttk.Label(panel, text="Interfaz de gestión de estaciones aquí").pack(padx=5, pady=5)
        return panel

    def gestionar_rutas_ui(self, parent_frame):
        """Panel de gestión de rutas (implementación básica)."""
        panel = ttk.LabelFrame(parent_frame, text="Gestión de Rutas", padding=10)
        ttk.Label(panel, text="Interfaz de gestión de rutas aquí").pack(padx=5, pady=5)
        return panel

    def deserializar_trenes(self, trenes_dict):
        """Convierte los diccionarios de trenes cargados (JSON) de vuelta a objetos Tren."""
        objetos_tren = {}
        for nombre, specs in trenes_dict.items():
            objetos_tren[nombre] = Tren(
                nombre=nombre,
                capacidad=specs['capacidad'],
                combustible=specs['combustible'],
                velocidad_max=specs['velocidad_max']
            )
        return objetos_tren

    def deserializar_pasajero(self, pasajero_dict):
        """Convierte un diccionario cargado de vuelta a un objeto Pasajero."""
        
        # 1. Convertir strings ISO 8601 a objetos datetime
        tiempo_llegada = dt.datetime.fromisoformat(pasajero_dict["tiempo_llegada"])
        
        tiempo_partida = None
        if pasajero_dict["tiempo_partida"]:
            tiempo_partida = dt.datetime.fromisoformat(pasajero_dict["tiempo_partida"])
            
        # 2. Crear el objeto Pasajero
        p = Pasajero(
            origen=pasajero_dict["origen"],
            destino=pasajero_dict["destino"],
            tiempo_llegada=tiempo_llegada
        )
        p.id = pasajero_dict["id"] # Restaurar el ID original
        p.tiempo_partida = tiempo_partida
        
        # 3. Asegurar que el contador estático no se pierda si este ID es el más alto
        if p.id >= Pasajero.id_counter:
            Pasajero.id_counter = p.id + 1
            
        return p

    def deserializar_estaciones(self, estaciones_dict):
        """
        Convierte los diccionarios de estaciones cargados (JSON) de vuelta a objetos Estacion,
        incluyendo la reconstrucción de pasajeros.
        """
        objetos_estacion = {}
        for nombre, specs in estaciones_dict.items():
            
            # 1. Crear la Estación
            estacion = Estacion(
                nombre=nombre,
                coordenada_x=specs['coord_x'],
                coordenada_y=specs['coord_y']
            )
            
            # 2. Reconstruir los Pasajeros
            if specs.get("pasajeros_esperando"):
                for p_dict in specs["pasajeros_esperando"]:
                    pasajero = self.deserializar_pasajero(p_dict)
                    estacion.agregar_pasajero(pasajero) # Agrega el objeto Pasajero a la lista
            
            objetos_estacion[nombre] = estacion
            
        return objetos_estacion
    
    def deserializar_rutas(self, rutas_lista):
        """Convierte una lista de tuplas de rutas cargadas de vuelta a una lista de objetos Ruta."""
        objetos_ruta = []
        for origen, destino, distancia in rutas_lista:
            objetos_ruta.append(Ruta(
                origen=origen,
                destino=destino,
                distancia_km=distancia
            ))
        return objetos_ruta

    def guardar_estado(self):
        """Método que llama a la función de guardado externo."""
        if guardar_datos(self.trenes, self.estaciones, self.rutas):
            tk.messagebox.showinfo("Guardado", "El estado del simulador ha sido guardado.")
        else:
            tk.messagebox.showerror("Error de Guardado", "No se pudo guardar el archivo de datos.")
    
    def crear_interfaz(self):
            
            menu_frame = ttk.Frame(self.master, padding="10 10 10 10")
            menu_frame.grid(row=0, column=0, sticky="nsew")
            menu_frame.grid_columnconfigure(0, weight=1)
            menu_frame.grid_columnconfigure(1, weight=1)
            self.master.grid_columnconfigure(1, weight=1)
            self.master.grid_columnconfigure(0, weight=0)
            self.master.grid_rowconfigure(0, weight=1)

            self.crear_menu_lateral()
            
            self.main_content_frame = ttk.Frame(self.master)
            self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

            self.main_content_frame.grid_columnconfigure(0, weight=1)
            self.main_content_frame.grid_rowconfigure(0, weight=1)

            self.paneles = {}
            self.crear_paneles_gestion()

            self.show_panel("Mapa")

            canvas = tk.Canvas(menu_frame, bg="#e0e0e0") 
            canvas.grid(row=0, column=0, columnspan=2, sticky="nsew") 
            menu_frame.grid_rowconfigure(0, weight=1)        
            
            left_menu = ttk.Frame(canvas, padding="10")
            canvas.create_window(150, 150, window=left_menu, anchor="center") 
            
    def crear_menu_lateral(self):
        """
        Crea el marco del menú lateral y coloca los botones de acción.
        """
        # 1. Crear el Frame que contendrá todos los botones (Columna 0 de la ventana principal)
        left_menu = ttk.Frame(self.master, padding="10")
        left_menu.grid(row=0, column=0, sticky="nsew")            
        botones_izq = [
                "Iniciar simulación", 
                "Acceder a datos de trenes", 
                "Acceder a datos de estación",
                "Acceder a datos de ruta",
                "Modificar datos",
                "GUARDAR ESTADO",
                "CARGAR ESTADO"
            ]
                    
        for i, text in enumerate(botones_izq):
            boton = ttk.Button(left_menu, text=text, command=lambda t=text: self.manejo_click_menu(t))
            boton.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
        left_menu.grid_columnconfigure(0, weight=1)
        self.left_menu = left_menu
            

    def crear_paneles(self):
        
        data_frame = ttk.Frame(self.master, padding="10")
        data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_columnconfigure(1, weight=1)
        data_frame.grid_columnconfigure(2, weight=1)
        data_frame.grid_rowconfigure(0, weight=1)

        map_panel = ttk.LabelFrame(data_frame, text="Rutas y Mapa")
        map_panel.grid(row=0, column=0, padx=5, sticky="nsew", columnspan=1)
        
        map_container = ttk.Frame(map_panel)
        map_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        v_scrollbar = ttk.Scrollbar(map_container, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(map_container, orient=tk.HORIZONTAL)
       
        self.map_canvas = tk.Canvas(map_container, bg="white", 
                                    yscrollcommand=v_scrollbar.set, 
                                    xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.map_canvas.yview)
        h_scrollbar.config(command=self.map_canvas.xview)
        
        self.map_canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")        
        
        map_container.grid_rowconfigure(0, weight=1)
        map_container.grid_columnconfigure(0, weight=1)        
        
        self.dibujar_mapa()
    
    def crear_map_panel(self, parent_frame):
        """
        Crea el marco, el Canvas y las barras de desplazamiento para el mapa de rutas.
        Retorna el marco principal del mapa.
        """
        # Marco principal del mapa
        map_panel = ttk.LabelFrame(parent_frame, text="Rutas y Mapa", padding=5)
        
        # 1. Configurar el contenedor (map_container) para que sea expandible
        map_container = ttk.Frame(map_panel)
        map_container.grid(row=0, column=0, sticky="nsew")
        
        # El map_panel y map_container deben expandirse dentro de sus padres
        map_panel.grid_columnconfigure(0, weight=1)
        map_panel.grid_rowconfigure(0, weight=1)
        
        # 2. Crear barras de desplazamiento (Scrollbars)
        v_scrollbar = ttk.Scrollbar(map_container, orient="vertical")
        h_scrollbar = ttk.Scrollbar(map_container, orient="horizontal")

        # 3. Crear el Canvas (Aquí es donde se dibujarán las estaciones y rutas)
        self.map_canvas = tk.Canvas(map_container, 
                                    bg="white", 
                                    yscrollcommand=v_scrollbar.set, 
                                    xscrollcommand=h_scrollbar.set)
                                    
        # 4. Configurar el Canvas para que se expanda
        self.map_canvas.grid(row=0, column=0, sticky="nsew")

        # 5. Colocar barras de desplazamiento y enlazarlas
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        v_scrollbar.config(command=self.map_canvas.yview)
        h_scrollbar.config(command=self.map_canvas.xview)
        
        # 6. Configurar la expansión del contenedor interno
        map_container.grid_rowconfigure(0, weight=1)
        map_container.grid_columnconfigure(0, weight=1)

        # Llamada inicial para dibujar el contenido (estaciones y rutas por defecto)
        self.dibujar_mapa() 

        return map_panel

    def crear_paneles_gestion(self):
        
        # --- Panel de Rutas y Mapa (Ya existente) ---
        # Este panel es el más complejo, por lo que puede tener su propia función.
        map_panel = self.crear_map_panel(self.main_content_frame) 
        self.paneles["mapa"] = map_panel
        # Colocamos en la misma celda, pero solo uno estará visible
        map_panel.grid(row=0, column=0, sticky="nsew") 

        # --- Panel de Gestión de Trenes ---
        # Si tienes una función gestionar_trenes_ui que devuelve un Frame:
        tren_panel = self.gestionar_trenes_ui(self.main_content_frame)
        self.paneles["trenes"] = tren_panel
        tren_panel.grid(row=0, column=0, sticky="nsew") # Mismo lugar que el mapa
        
        # --- Panel de Gestión de Estaciones ---
        estacion_panel = self.gestionar_estaciones_ui(self.main_content_frame)
        self.paneles["estaciones"] = estacion_panel
        estacion_panel.grid(row=0, column=0, sticky="nsew") # Mismo lugar
        
        # --- Panel de Gestión de Rutas (La lista de rutas, no el mapa) ---
        rutas_panel = self.gestionar_rutas_ui(self.main_content_frame)
        self.paneles["rutas"] = rutas_panel
        rutas_panel.grid(row=0, column=0, sticky="nsew") # Mismo lugar

        # Inicialmente, ocultamos todos excepto el mapa
        self.show_panel("mapa")
        
    def show_panel(self, panel_name):
        """Muestra el panel solicitado y oculta todos los demás."""
        
        target_panel = self.paneles.get(panel_name)
        if not target_panel:
            print(f"Error: Panel '{panel_name}' no encontrado.")
            return

        # Ocultar todos los paneles
        for name, panel in self.paneles.items():
            # Usamos grid_remove para ocultar el widget sin perder la configuración de grid
            panel.grid_remove() 
            
        # Mostrar el panel deseado
        target_panel.grid()

    def dibujar_mapa(self):
        
        """Dibuja las estaciones y rutas y configura el scrollregion del canvas."""
        if not self.map_canvas:
            return
            
        self.map_canvas.delete("all") # Limpiar dibujos anteriores
        
        radio = 5
        estacion_coords = []
        
        # 1. Dibujar Rutas (Líneas)
        for ruta in self.rutas:
            # Accedemos a los atributos del objeto Ruta
            origen = ruta.origen
            destino = ruta.destino
            
            # Buscamos las coordenadas de las estaciones (que son objetos Estacion)
            if origen in self.estaciones and destino in self.estaciones:
                # Usamos los atributos del objeto Estacion
                x1, y1 = self.estaciones[origen].coordenada_x, self.estaciones[origen].coordenada_y
                x2, y2 = self.estaciones[destino].coordenada_x, self.estaciones[destino].coordenada_y
                
                self.map_canvas.create_line(x1, y1, x2, y2, 
                                            dash=(4, 2), width=2, fill="gray")
        
        # 2. Dibujar Estaciones (Círculos y Etiquetas)
        for nombre, estacion in self.estaciones.items():
            # Usamos los atributos del objeto Estacion
            x, y = estacion.coordenada_x, estacion.coordenada_y
            
            # Dibujar el círculo y texto
            self.map_canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                        fill="blue", outline="black")
            self.map_canvas.create_text(x, y - 15, text=nombre, anchor=tk.S, fill="black")
            
            estacion_coords.append(x)
            estacion_coords.append(y)
            
        # 3. Configurar el área de desplazamiento (Scrollregion)
        # ... (código para configurar el scrollregion, se mantiene igual)
        if estacion_coords:
            min_x = min(estacion_coords) - 50
            min_y = min(estacion_coords) - 50
            max_x = max(estacion_coords) + 50
            max_y = max(estacion_coords) + 50
        else:
             min_x, min_y, max_x, max_y = 0, 0, 500, 500
        
        self.map_canvas.config(scrollregion=(min_x, min_y, max_x, max_y))

    def manejo_click_menu(self, action_nombre):
        print(f"DEBUG: Se hizo clic en: {action_nombre}")
        
        if action_nombre == "Iniciar simulación":
            self.iniciar_simulacion()
        elif action_nombre == "Acceder a datos de trenes":
            self.show_panel("trenes")
        elif action_nombre == "Acceder a datos de estaciones":
            self.show_panel("estaciones")
        elif action_nombre == "Acceder a datos de rutas":
            self.show_panel("rutas")
        elif action_nombre == "Modificar datos":
            self.modificar_datos()
        elif action_nombre == "Modificar datos":
            self.modificar_datos()
        elif action_nombre == "GUARDAR ESTADO": 
            self.guardar_estado()
        elif action_nombre == "CARGAR ESTADO": 
            self.cargar_estado()
        else:
            print(f"ADVERTENCIA: Acción '{action_nombre}' no implementada.")
        


    def iniciar_simulacion(self):
        print("INICIANDO SIMULACIÓN...")
        import tkinter.messagebox as messagebox

        if not self.trenes or not self.estaciones:
            messagebox.showwarning("Error de Simulación", "Debe tener al menos un tren y una estación definidos para iniciar.")
            return
        
        total_estaciones = len(self.estaciones)
        total_rutas = len(self.rutas)
        
        mensaje = (
            f"Simulación de Trenes Iniciada.\n"
            f"Parámetros cargados:\n"
            f"- Tipos de trenes: {len(self.trenes)}\n"
            f"- Estaciones: {total_estaciones}\n"
            f"- Rutas definidas: {total_rutas}\n\n"
            f"El motor de simulación está calculando los trayectos..."
        )
        messagebox.showinfo("Simulación en Curso", mensaje)

    def mostrar_datos(self, tipo_dato):
        print(f"MOSTRANDO DATOS: {tipo_dato}")
        datos = None
        columnas = []        
        
        if tipo_dato == "Trenes":
            datos = self.trenes
            columnas = ["ID", "Tipo de Tren"]
        elif tipo_dato == "Estación":
            datos = self.estaciones.keys()
            columnas = ["Estación", "Coordenadas X", "Coordenadas Y"]
        elif tipo_dato == "Ruta":
            datos = self.rutas
            columnas = ["Origen", "Destino", "Distancia (km)"]
        else:
            return
       
        data_window = tk.Toplevel(self.master)
        data_window.title(f"Datos de {tipo_dato}")        
        
        tree = ttk.Treeview(data_window, columns=columnas, show='headings')        
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)            
        
        if tipo_dato == "Trenes":
            datos = self.trenes.items() 
            columnas = ["Nombre", "Capacidad", "Combustible", "Velocidad Máx (km/h)"]
            
        elif tipo_dato == "Estación":
            for nombre, coords in self.estaciones.items():
                tree.insert("", tk.END, values=(nombre, coords[0], coords[1]))
        elif tipo_dato == "Ruta":
            for ruta in datos:
                tree.insert("", tk.END, values=ruta)
                
        tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        if tipo_dato == "Trenes":
            for nombre, specs in datos:
                tree.insert("", tk.END, values=(nombre, 
                                                specs['capacidad'], 
                                                specs['combustible'], 
                                                specs['velocidad_max']))
        
    def modificar_datos(self):
        from config.ModificarDatos import modificar_datos
        modificar_datos(self)
        
    def gestionar_trenes(self):
        from config.ModificarTrenes import gestionar_trenes
        gestionar_trenes(self)
        def agregar_tren():
            from config.ModificarTrenes import agregar_tren
            agregar_tren(self)
        def quitar_tren():
            from config.ModificarTrenes import quitar_tren
            quitar_tren(self)
    def actualizar_trenes(self, listbox):
        from config.ModificarTrenes import actualizar_trenes
        actualizar_trenes(self, listbox)

    def gestionar_estaciones(self):
        from config.ModificarEstaciones import gestionar_estaciones
        gestionar_estaciones(self)
        def añadir_estación():
            from config.ModificarEstaciones import añadir_estación
            añadir_estación(self)
        def quitar_estación():
            from config.ModificarEstaciones import quitar_estación
            quitar_estación(self)
    def actualizar_estaciones(self, listbox):
        from config.ModificarEstaciones import actualizar_estaciones
        actualizar_estaciones(self, listbox)
    
    def gestionar_rutas(self):
        from config.ModificarRutas import gestionar_rutas
        gestionar_rutas(self)
        def añadir_ruta():
            from config.ModificarRutas import añadir_ruta
            añadir_ruta(self)
        def quitar_ruta():
            from config.ModificarRutas import quitar_ruta
            quitar_ruta(self)
    def actualizar_rutas(self, listbox):
        from config.ModificarRutas import Actualizar_rutas
        Actualizar_rutas(self, listbox)
        
    def crear_panel_listas(self, parent_frame, title, items):
        list_frame = ttk.LabelFrame(parent_frame, text=title, padding="5")
        
        for item in items:
            list_item = ttk.Frame(list_frame)
            list_item.pack(fill='x', pady=2)
            ttk.Label(list_item, text=f"- {item} -").pack(side="left")
            ttk.Checkbutton(list_item, text="").pack(side="right") 
            
            ttk.Button(list_frame, text="+", width=3, command=lambda: print(f"Añadir a {title}")).pack(pady=5)
        
            return list_frame

if __name__ == '__main__':
    root = tk.Tk()
    app = SimuladorTrenes(root)
    root.mainloop()