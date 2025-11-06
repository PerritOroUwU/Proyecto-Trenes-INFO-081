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
    
    boton_prueba = tk.Button(
        frame_prueba,
        text="Botón de Prueba",
        command=prueba_de_acción_de_boton,
        width=20,
        height=2
    )
    boton_prueba.pack(pady=15)
    
    boton_prueba2 = tk.Button(
        frame_prueba,
        text="Botón de Prueba 2",
        command=lambda: print("¡Botón 2 presionado!"),
        width=20,
        height=2
    )
    boton_prueba2.pack(pady=15)
    
    boton_prueba3 = tk.Button(
        frame_prueba,
        text="Botón de Prueba 3",
        command=lambda: print("¡Botón 3 presionado!"),
        width=20,
        height=2
    )
    boton_prueba3.pack(pady=15)
    
    boton_prueba4 = tk.Button(
        frame_prueba,
        text="Botón de Prueba 4",
        command=lambda: print("¡Botón 4 presionado!"),
        width=20,
        height=2
    )
    boton_prueba4.pack(pady=15)
    
    boton_prueba5 = tk.Button(
        frame_prueba,
        text="Botón de Prueba 5",
        command=lambda: print("¡Botón 5 presionado!"),
        width=20,
        height=2
    )
    boton_prueba5.pack(pady=15)

    frame_prueba.pack_propagate(0) # Evita que el frame cambie de tamaño
    root.mainloop()

if __name__ == "__main__":
    main()