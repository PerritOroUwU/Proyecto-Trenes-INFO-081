import tkinter as tk
from tkinter import ttk

def gestionar_trenes(self):
        import tkinter.messagebox as messagebox
        
        ventana_trenes = tk.Toplevel(self.master)
        ventana_trenes.title("Gestionar Tipos de Trenes")

        añadir_frame = ttk.LabelFrame(ventana_trenes, text="Añadir Nuevo Tren", padding=10)
        añadir_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(añadir_frame, text="Nombre/Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        nombre_entrada = ttk.Entry(añadir_frame, width=20)
        nombre_entrada.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Capacidad (Pax):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        entrada_capacidad = ttk.Entry(añadir_frame, width=20)
        entrada_capacidad.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Vel. Máx (km/h):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        entrada_velocidad = ttk.Entry(añadir_frame, width=20)
        entrada_velocidad.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Combustible:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        combustible_options = ["Diésel", "Eléctrico", "Híbrido", "Otro"]
        combustible_cb = ttk.Combobox(añadir_frame, values=combustible_options, state='readonly', width=18)
        combustible_cb.set(combustible_options[0]) 
        combustible_cb.grid(row=3, column=1, padx=5, pady=5)

        def agregar_tren():
            nuevo_Tren = nombre_entrada.get().strip().upper()
            combustible = combustible_cb.get()
            
            try:
                capacidad = int(entrada_capacidad.get())
                velocidad = int(entrada_velocidad.get())
                
                if nuevo_Tren and nuevo_Tren not in self.trenes and capacidad > 0 and velocidad > 0:
                    self.trenes[nuevo_Tren] = {
                        "capacidad": capacidad, 
                        "combustible": combustible, 
                        "velocidad_max": velocidad
                    }
                    self.actualizar_trenes(lista_trenes) 
                    messagebox.showinfo("Éxito", f"Tren '{nuevo_Tren}' añadido con especificaciones.")
                    nombre_entrada.delete(0, tk.END)
                    entrada_capacidad.delete(0, tk.END)
                    entrada_velocidad.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", "Datos no válidos, el tren ya existe, o valores de capacidad/velocidad no son positivos.")
            except ValueError:
                messagebox.showerror("Error", "Capacidad y Velocidad Máxima deben ser números enteros.")

        ttk.Button(añadir_frame, text="Añadir Tren", command=agregar_tren).grid(row=4, columnspan=2, pady=10)
        
        quitar_frame = ttk.LabelFrame(ventana_trenes, text="Quitar Tren Existente", padding=10)
        quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)

        lista_trenes = tk.Listbox(quitar_frame)
        lista_trenes.pack(fill='both', expand=True, padx=5, pady=5)

        def quitar_tren():
            try:
                index = lista_trenes.curselection()[0]
                tren_str = lista_trenes.get(index)
                tren_a_quitar = tren_str.split(" (")[0]
                
                del self.trenes[tren_a_quitar]
                
                self.actualizar_trenes(lista_trenes)
                messagebox.showinfo("Éxito", f"Tren '{tren_a_quitar}' eliminado.")
            except IndexError:
                messagebox.showerror("Error", "Seleccione un tren para eliminar.")
            except KeyError:
                 messagebox.showerror("Error", "Error al encontrar el tren.")

        ttk.Button(quitar_frame, text="Quitar Tren Seleccionado", command=quitar_tren).pack(pady=5)
        
        self.actualizar_trenes(lista_trenes)

def actualizar_trenes(self, listbox):
    listbox.delete(0, tk.END) 
    for nombre, specs in self.trenes.items():
        display_text = (
            f"{nombre} (Cap: {specs['capacidad']}, "
            f"Comb: {specs['combustible']}, "
            f"Vel: {specs['velocidad_max']} km/h)"
        )
        listbox.insert(tk.END, display_text)