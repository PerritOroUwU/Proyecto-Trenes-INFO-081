import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Ventana de Prueba")
    root.geometry("1024x600") # Establece el tamaño de la ventana en píxeles
    frame_prueba = tk.Frame(
        root,
        bg="lightblue",
        width=350,
        height=375,
        bd=5,
        relief="raised"
    )
    frame_prueba.pack(side="left", padx=10, pady=20)
    def prueba_de_acción_de_boton():
        ventana_prueba = tk.Toplevel(root)
        ventana_prueba.geometry("1024x600")
        ventana_prueba.title("Simulación Iniciada")
        etiqueta = tk.Label(
            ventana_prueba,
            text="Simulación en curso...",
            font=("Arial", 24)
        )
        etiqueta.pack(pady=20)

    boton_prueba = tk.Button(
        frame_prueba,
        text="Iiniciar Simulación",
        command=prueba_de_acción_de_boton,
        width=25,
        height=2
    )
    boton_prueba.pack(pady=15)

    boton_prueba2 = tk.Button(
        frame_prueba,
        text="Acceso a datos de trenes",
        command=prueba_de_acción_de_boton,
        width=25,
        height=2
    )
    boton_prueba2.pack(pady=15)
        
    boton_prueba3 = tk.Button(
        frame_prueba,
        text="Acceder a datos de estaciones",
        command=prueba_de_acción_de_boton,
        width=25,
        height=2
    )
    boton_prueba3.pack(pady=15)
    
    boton_prueba4 = tk.Button(
        frame_prueba,
        text="Acceder a datos de rutas",
        command=prueba_de_acción_de_boton,
        width=25,
        height=2
    )
    boton_prueba4.pack(pady=15)
    
    boton_prueba5 = tk.Button(
        frame_prueba,
        text="Modificar datos de simulación",
        command=prueba_de_acción_de_boton,
        width=25,
        height=2
    )
    boton_prueba5.pack(pady=15)

    frame_prueba.pack_propagate(0) # Evita que el frame cambie de tamaño
    root.mainloop()

if __name__ == "__main__":
    main()