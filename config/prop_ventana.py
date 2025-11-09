import tkinter as tk
root = tk.Tk()
class configuracion:
    def get_config():
        root = tk.Tk()
        tam_ventana = root.geometry("1024x600") #tamaño de ventana
        azul_claro = bg="#ADD8E6", #color de fondo
        grosor_borde = bd=10 #que tan grande son los bordes
        padingx = padx=10
        padingy = pady=20 
        #"Espacio en pixeles de separacion cada widget"  
#REVISAR