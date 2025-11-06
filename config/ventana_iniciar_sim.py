import tkinter as tk
import datetime as dt
#HORA = dt.datetime
hora_actual = dt.datetime.now
#agregar hora de ejemplo mas tarde
def main():
   root = tk.Tk()
   root.title("Prueba de menu inicio sim")
   root.geometry("1024x600")
   
   etiqueta_hora = tk.Label(root,
                          text=hora_actual,
                          foreground= "White",
                          bg="#006666",
                          font=("Arial", 16),
                          width=20,
                          height=3
                          )
   etiqueta_hora.pack(anchor="nw",padx=30,pady=5)
   frame_prueba = tk.Frame(
        root,
        bg="lightblue",
        width=350,
        height=375,
        bd=5,
        relief="raised"
    )
   frame_prueba.pack(side="left", padx=10, pady=20)
   #me falta revisar en donde esta el label exactamente para agregarle texto
   etiqueta_hora = tk.Label(root,
                          text=hora_actual,
                          foreground= "White",
                          bg="#006666",
                          font=("Arial", 16),
                          width=20,
                          height=3
                          )
   #falta texto con la capacidad y lo de eventos
   #pero ahi se crean algo xd
   root.mainloop()
if __name__ == "__main__":
    main()