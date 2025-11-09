import tkinter as tk
from tkinter import messagebox as msgbox


def main():
   root = tk.Tk()
   root.title("messageboxes")
   root.geometry("1024x600")
   cantidad_saludos = 0

   def saluda():
       nonlocal cantidad_saludos  # para que no intente usar una var local
       cantidad_saludos += 1
       msgbox.showinfo("Saludos", f"Saludé {str(cantidad_saludos)} veces")

   def termina():
       if msgbox.askyesno("Salir", "¿Desea terminar con nuestro sufrimiento?"):
           root.destroy()

   tk.Button(root, text="saludar", command=saluda).pack(side=tk.LEFT)
   tk.Button(root, text="terminar", command=termina).pack()
   root.mainloop()

if __name__ == "__main__":
   main()

   #Usar esto de alguna manera para un mensaje de confirmación al salir