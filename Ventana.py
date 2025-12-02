import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
from logic.Guardado import guardar_datos, cargar_datos
from models.rutas import __init__

class SimuladorTrenes:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Trenes")        
        
        master.geometry("900x700")

        data = cargar_datos()

        if not data["trenes"] and not data["estaciones"] and not data["rutas"]:
            self.trenes = { "BHU": {"capacidad": 150, "combustible": "Diésel", "velocidad_max": 120}, 
                           "EMU": {"capacidad": 300, "combustible": "Eléctrico", "velocidad_max": 160}
                           }
            self.estaciones = { "Estación central": (50, 200), 
                               "Rancagua": (150, 300), 
                               "Talca": (300, 100), 
                               "Chillán": (450, 400)
                               }
            self.rutas = __init__
        else:
            self.trenes = data["trenes"]
            self.estaciones = data["estaciones"]
            self.rutas = data["rutas"]

        self.trenes = {
            "BHU": {"capacidad": 150, "combustible": "Diésel", "velocidad_max": 120},
            "EMU": {"capacidad": 300, "combustible": "Eléctrico", "velocidad_max": 160}
        }

        self.estaciones = {
            "Santiago": (50, 200),
            "Rancagua": (150, 300),
            "Talca": (300, 100),
            "Chillán": (450, 400)
        }

        self.rutas = [
            ("Santiago", "Rancagua", 80), 
            ("Rancagua", "Talca", 150),
            ("Talca", "Chillán", 100)
        ]
        
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=2) 
        master.grid_rowconfigure(1, weight=1) 
        
        self.crear_interfaz()
        self.crear_paneles()
        self.map_canvas = None

    class GeneradorUniforme(Generador):
        from Ppdc_timed_generator.generadores import generador, generador_uniforme
        generador_uniforme.generar_clientes()

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
            
            canvas = tk.Canvas(menu_frame, bg="#e0e0e0") 
            canvas.grid(row=0, column=0, columnspan=2, sticky="nsew") 
            menu_frame.grid_rowconfigure(0, weight=1)        
            
            left_menu = ttk.Frame(canvas, padding="10")
            canvas.create_window(150, 150, window=left_menu, anchor="center") 
            
            botones_izq = [
                "Iniciar simulación", 
                "Acceder a datos de trenes", 
                "Acceder a datos de estación",
                "Acceder a datos de ruta",
                "Modificar datos",
                "GUARDAR ESTADO"
            ]
                    
            for i, text in enumerate(botones_izq):
                boton = ttk.Button(left_menu, text=text, command=lambda t=text: self.manejo_click_menu(t))
                boton.pack(fill='x', pady=5)
            
            right_menu = ttk.Frame(canvas, padding="10")
            canvas.create_window(650, 150, window=right_menu, anchor="center") 
           
            botones_der = [
                "Acceder a datos de trenes", 
                "Acceder a datos de estación",
                "Acceder a datos de ruta"
            ]
        
            for text in botones_der:
                boton = ttk.Button(right_menu, text=text, command=lambda t=text: print(f"Presionado: {t}"))
                boton.pack(fill='x', pady=5)

    def crear_paneles(self):
        
        data_frame = ttk.Frame(self.master, padding="10")
        data_frame.grid(row=1, column=0, sticky="nsew")

        data_frame.grid_columnconfigure(0, weight=1)
        
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
        
    def dibujar_mapa(self):
        
        if not self.map_canvas:
            return
            
        self.map_canvas.delete("all") 

        min_x, min_y = 0, 0
        max_x, max_y = 500, 500         
        
        for origen, destino, _ in self.rutas:
            if origen in self.estaciones and destino in self.estaciones:
                x1, y1 = self.estaciones[origen]
                x2, y2 = self.estaciones[destino]
                self.map_canvas.create_line(x1, y1, x2, y2, 
                                            dash=(4, 2), width=2, fill="gray")
        
        radio = 5
        estacion_coords = []
        for nombre, (x, y) in self.estaciones.items():
            self.map_canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                        fill="blue", outline="black")
            self.map_canvas.create_text(x, y - 15, text=nombre, anchor=tk.S, fill="black")
            
            estacion_coords.append(x)
            estacion_coords.append(y)
        
        if estacion_coords:
            min_x = min(estacion_coords) - 50
            min_y = min(estacion_coords) - 50
            max_x = max(estacion_coords) + 50
            max_y = max(estacion_coords) + 50        
        
        self.map_canvas.config(scrollregion=(min_x, min_y, max_x, max_y))

    def manejo_click_menu(self, action_nombre):
        print(f"DEBUG: Se hizo clic en: {action_nombre}")
        
        if action_nombre == "Iniciar simulación":
            self.iniciar_simulacion()
        elif "datos de trenes" in action_nombre:
            self.mostrar_datos("Trenes")
        elif "datos de estación" in action_nombre:
            self.mostrar_datos("Estación")
        elif "datos de ruta" in action_nombre:
            self.mostrar_datos("Ruta")
        elif action_nombre == "Modificar datos":
            self.modificar_datos()
        elif action_nombre == "Modificar datos":
            self.modificar_datos()
        elif action_nombre == "GUARDAR ESTADO": # <--- NUEVA LÓGICA
            self.guardar_estado()
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




