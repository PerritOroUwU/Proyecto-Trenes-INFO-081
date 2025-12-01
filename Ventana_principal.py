import tkinter as tk
from UI.ventanas import acción_de_boton


def main():
    root = tk.Tk()
    root.title("Ventana Principal")
    root.geometry("1024x600") # Establece el tamaño de la ventana en píxeles
    frame_menu = tk.Frame(
        root,
        bg="lightblue",
        width=350,
        height=375,
        bd=5,
        relief="raised"
    )
    frame_menu.pack(side="left", padx=10, pady=20)
    
    boton_IS = tk.Button(
        frame_menu,
        text="Iniciar Simulación",
        command=acción_de_boton,
        width=25,
        height=2
    )
    boton_IS.pack(pady=15)

    boton_ADT = tk.Button(
        frame_menu,
        text="Acceso a datos de trenes",
        command=acción_de_boton,
        width=25,
        height=2
    )
    boton_ADT.pack(pady=15)
        
    boton_ADE = tk.Button(
        frame_menu,
        text="Acceder a datos de estaciones",
        command=acción_de_boton,
        width=25,
        height=2
    )
    boton_ADE.pack(pady=15)
    
    boton_AR = tk.Button(
        frame_menu,
        text="Acceder a datos de rutas",
        command=acción_de_boton_rutas,
        width=25,
        height=2
    )
    boton_AR.pack(pady=15)
    
    boton_MDS = tk.Button(
        frame_menu,
        text="Modificar datos de simulación",
        command=acción_de_boton,
        width=25,
        height=2
    )
    boton_MDS.pack(pady=15)

    frame_menu.pack_propagate(0) # Evita que el frame cambie de tamaño
    root.mainloop()

if __name__ == "__main__":
    main()