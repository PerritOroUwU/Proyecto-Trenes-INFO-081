import tkinter as tk
from tkinter import ttk

def gestionar_rutas(self):
        import tkinter.messagebox as messagebox
        
        ventana_rutas = tk.Toplevel(self.master)
        ventana_rutas.title("Gestionar Rutas")

        añadir_frame = ttk.LabelFrame(ventana_rutas, text="Añadir Nueva Ruta", padding=10)
        añadir_frame.pack(padx=10, pady=10, fill='x')
        
        estacion_nombres = sorted(self.estaciones.keys())
        
        ttk.Label(añadir_frame, text="Origen:").grid(row=0, column=0, padx=5, pady=5)
        origen_cb = ttk.Combobox(añadir_frame, values=estacion_nombres, state='readonly')
        origen_cb.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Destino:").grid(row=1, column=0, padx=5, pady=5)
        destino_cb = ttk.Combobox(añadir_frame, values=estacion_nombres, state='readonly')
        destino_cb.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(añadir_frame, text="Distancia (km):").grid(row=2, column=0, padx=5, pady=5)
        entrada_distancia = ttk.Entry(añadir_frame)
        entrada_distancia.grid(row=2, column=1, padx=5, pady=5)
        
        def añadir_ruta():
            origen = origen_cb.get()
            destino = destino_cb.get()
            
            try:
                distancia = int(entrada_distancia.get())
                
                if origen and destino and origen != destino and distancia > 0:
                    nuevaRuta = (origen, destino, distancia)
                    if nuevaRuta not in self.rutas and (destino, origen, distancia) not in self.rutas:
                        self.rutas.append(nuevaRuta)
                        self.Actualizar_rutas(ruta_listbox)
                        self.dibujar_mapa()
                        messagebox.showinfo("Éxito", f"Ruta {origen}-{destino} añadida.")
                    else:
                        messagebox.showerror("Error", "La ruta ya existe o es inválida (Origen = Destino).")
                else:
                    messagebox.showerror("Error", "Seleccione origen/destino válidos e ingrese una distancia positiva.")
            except ValueError:
                messagebox.showerror("Error", "La distancia debe ser un número entero.")

        ttk.Button(añadir_frame, text="Añadir Ruta", command=añadir_ruta).grid(row=3, columnspan=2, pady=10)
        
        quitar_frame = ttk.LabelFrame(ventana_rutas, text="Quitar Ruta Existente", padding=10)
        quitar_frame.pack(padx=10, pady=10, fill='both', expand=True)

        ruta_listbox = tk.Listbox(quitar_frame)
        ruta_listbox.pack(fill='both', expand=True)

        def quitar_ruta():
            try:
                index = ruta_listbox.curselection()[0]
                ruta_str = ruta_listbox.get(index)
                
                parts = ruta_str.split(" -> ")
                origen = parts[0].strip()
                
                parts2 = parts[1].split(" (")
                destino = parts2[0].strip()
                distancia = int(parts2[1].replace(" km)", ""))
                
                ruta_a_quitar = (origen, destino, distancia)
                
                if ruta_a_quitar in self.rutas:
                    self.rutas.remove(ruta_a_quitar)
                else:
                    self.rutas = [r for r in self.rutas if not (r[0] == destino and r[1] == origen and r[2] == distancia)]
                
                self.Actualizar_rutas(ruta_listbox)
                self.dibujar_mapa()
                messagebox.showinfo("Éxito", f"Ruta {origen}-{destino} eliminada.")
            except IndexError:
                messagebox.showerror("Error", "Seleccione una ruta para eliminar.")
            except Exception:
                messagebox.showerror("Error", "Error al procesar la ruta seleccionada.")

        ttk.boton(quitar_frame, text="Quitar Ruta Seleccionada", command=quitar_ruta).pack(pady=5)
        
        self.Actualizar_rutas(ruta_listbox)

def Actualizar_rutas(self, listbox):
    listbox.delete(0, tk.END)
    for origen, destino, distancia in self.rutas:
        listbox.insert(tk.END, f"{origen} -> {destino} ({distancia} km)")