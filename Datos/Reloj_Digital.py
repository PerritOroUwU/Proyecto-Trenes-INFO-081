import tkinter as tk
import time

ventana = tk.Tk()
ventana.title("Reloj Digital")

#funcion para actualizar el reloj
def actualizar_reloj():
    hora_actual = time.strftime("%H:%M:%S")
    etiqueta.config(text = hora_actual)
    etiqueta.after(1000,actualizar_reloj)
#etiqueta para mostrar hora
etiqueta = tk.Label(ventana, font = ("Arial",50), bg = "black", fg = "white")
etiqueta.pack(anchor = "center")

actualizar_reloj()
ventana.mainloop()
