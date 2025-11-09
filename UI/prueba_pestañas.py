import tkinter as tk
from tkinter import ttk

Pestaña = tk.Tk()
Pestaña.title("INFO-081 - Proyecto Trenes")
Pestaña.geometry("1024x600")
notebook = ttk.Notebook(Pestaña)
notebook.pack(expand=True, fill='both')
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)

tk.Label(frame1, text="Contenido de la Pestaña 1").pack(pady=20)
tk.Button(frame1, text="Botón en Pestaña 1").pack(pady=10)

tk.Label(frame2, text="Contenido de la Pestaña 2").pack(pady=20)
tk.Entry(frame2).pack(pady=10)

tk.Label(frame3, text="Contenido de la Pestaña 3").pack(pady=20)
tk.Checkbutton(frame3, text="Opción en Pestaña 3").pack(pady=10)

notebook.add(frame1, text='Pestaña 1')
notebook.add(frame2, text='Pestaña 2')
notebook.add(frame3, text='Pestaña 3')

Pestaña.mainloop()