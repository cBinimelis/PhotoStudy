import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


#root = tk.Tk()
root=ttk.Window(themename='superhero')
root.title("Prueba de espacios")
root.resizable(False,False)
root.maxsize(400,700)
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)

top_frame=ttk.Frame(root)

folder_button=ttk.Button(top_frame, text="Buscar Carpeta")
viewer_frame=ttk.Frame(top_frame, borderwidth=1, height=500,width=400)

img1=ImageTk.PhotoImage(Image.open('demo.jpg').resize((380,520)))
label =ttk.Label(viewer_frame, image=img1)

#Seleccion de imagen
button_frame=ttk.Frame(top_frame,borderwidth=1)
btn_back=ttk.Button(button_frame, text='Anterior', bootstyle=SUCCESS)
btn_exit=ttk.Button(button_frame,text='Salir', bootstyle=DANGER)
btn_forward=ttk.Button(button_frame, text='Siguiente', bootstyle=SUCCESS)
#Seleccion de tiempo
time_frame=ttk.Frame(top_frame,borderwidth=1)

button1 = ttk.Button(time_frame, text="30 seg", bootstyle=(PRIMARY, OUTLINE))
button2 = ttk.Button(time_frame, text="1 min", bootstyle=(INFO, OUTLINE))
button3 = ttk.Button(time_frame, text="2 min", bootstyle=(PRIMARY, OUTLINE))
button4 = ttk.Button(time_frame, text="5 min", bootstyle=(INFO, OUTLINE))
button5 = ttk.Button(time_frame, text="10 min", bootstyle=(PRIMARY, OUTLINE))
#--------------------POSICIONAMIENTO--------------------#
#Posición contenedor principal
top_frame.grid(column=0, row=0)

#Posicion boton para seleccionar carpeta
folder_button.grid(column=0, row=1,columnspan=3, sticky=EW)

#Posicion visor de imagenes
viewer_frame.grid(column=0,row=2,columnspan=3)
label.grid(row=0, column=0, columnspan=3)

#Posicion botones inferiores
button_frame.grid(column=0,row=3,columnspan=3, sticky=NSEW)
btn_back.grid(column=0,row=0, sticky=NSEW)
btn_exit.grid(column=1,row=0, sticky=NSEW)
btn_forward.grid(column=2,row=0, sticky=NSEW)

button_frame.columnconfigure(0,weight=1)
button_frame.columnconfigure(1,weight=1)
button_frame.columnconfigure(2,weight=1)


#Seleccion de tiempo
time_frame.grid(column=0,row=4,columnspan=3, sticky=NSEW)
button1.grid(column=0,row=0, sticky=NSEW)
button2.grid(column=1,row=0, sticky=NSEW)
button3.grid(column=2,row=0, sticky=NSEW)
button4.grid(column=3,row=0, sticky=NSEW)
button5.grid(column=4,row=0, sticky=NSEW)


time_frame.columnconfigure(0,weight=1)
time_frame.columnconfigure(1,weight=1)
time_frame.columnconfigure(2,weight=1)
time_frame.columnconfigure(3,weight=1)
time_frame.columnconfigure(4,weight=1)

#messagebox.showinfo(message="Mensaje", title="Título")

root.mainloop()