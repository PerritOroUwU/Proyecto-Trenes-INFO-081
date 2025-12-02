import tkinter as tk
from tkinter import ttk


def gestionar_estaciones(self):
        import tkinter.messagebox as messagebox
        
        estaciones_window = tk.Toplevel(self.master)
        estaciones_window.title("Gestionar Estaciones")

        añadir_frame = ttk.LabelFrame(estaciones_window, text="Añadir Nueva Estación", padding=10)
        añadir_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(añadir_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_entrada = ttk.Entry(añadir_frame)
        nombre_entrada.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Coord. X (0-500):").grid(row=1, column=0, padx=5, pady=5)
        x_entry = ttk.Entry(añadir_frame)
        x_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Coord. Y (0-500):").grid(row=2, column=0, padx=5, pady=5)
        y_entry = ttk.Entry(añadir_frame)
        y_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def añadir_estación():
            nombre = nombre_entrada.get().strip()
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                
                if nombre and nombre not in self.estaciones and 0 <= x <= 500 and 0 <= y <= 500:
                    self.estaciones[nombre] = (x, y)
                    self.actualizar_estaciones(station_listbox)
                    self.dibujar_mapa()
                    nombre_entrada.delete(0, tk.END)
                    x_entry.delete(0, tk.END)
                    y_entry.delete(0, tk.END)
                    messagebox.showinfo("Éxito", f"Estación '{nombre}' añadida en ({x}, {y}).")
                else:
                    messagebox.showerror("Error", "Datos no válidos o estación ya existe. Coordenadas deben ser entre 0 y 500.")
            except ValueError:
                messagebox.showerror("Error", "Las coordenadas deben ser números enteros.")

        ttk.Button(añadir_frame, text="Añadir Estación", command=añadir_estación).grid(row=3, columnspan=2, pady=10)
        
        quitar_frame = ttk.LabelFrame(estaciones_window, text="Quitar Estación Existente", padding=10)
        quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)

        station_listbox = tk.Listbox(quitar_frame)
        station_listbox.pack(fill='both', expand=True)

        def quitar_estación():
            try:
                index = station_listbox.curselection()[0]
                estación_a_quitar = station_listbox.get(index)
                
                del self.estaciones[estación_a_quitar]
                
                self.rutas = [r for r in self.rutas if r[0] != estación_a_quitar and r[1] != estación_a_quitar]
                
                self.actualizar_estaciones(station_listbox)
                self.dibujar_mapa()
                messagebox.showinfo("Éxito", f"Estación '{estación_a_quitar}' y sus rutas eliminadas.")
            except IndexError:
                messagebox.showerror("Error", "Seleccione una estación para eliminar.")

        ttk.Button(quitar_frame, text="Quitar Estación Seleccionada", command=quitar_estación).pack(pady=5)
        
        self.actualizar_estaciones(station_listbox)

def actualizar_estaciones(self, listbox):
    listbox.delete(0, tk.END)
    for station, coords in self.estaciones.items():
        listbox.insert(tk.END, f"{station} ({coords[0]}, {coords[1]})")