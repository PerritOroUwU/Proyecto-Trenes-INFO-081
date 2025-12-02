import tkinter as tk
from tkinter import ttk

def modificar_datos(self):
    print("MODIFICANDO DATOS...")
    mod_window = tk.Toplevel(self.master)
    mod_window.title("Panel de Gestión de Datos")
    mod_window.geometry("400x300")
        
    ttk.Label(mod_window, text="Seleccione qué desea gestionar:", font=('Arial', 12, 'bold')).pack(pady=15)
        
    ttk.Button(mod_window, text="Gestionar Trenes", 
                command=self.gestionar_trenes).pack(fill='x', padx=50, pady=5)
                   
    ttk.Button(mod_window, text="Gestionar Estaciones", 
                command=self.gestionar_estaciones).pack(fill='x', padx=50, pady=5)
                   
    ttk.Button(mod_window, text="Gestionar Rutas", 
                command=self.gestionar_rutas).pack(fill='x', padx=50, pady=5)