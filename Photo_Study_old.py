from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

root=Tk()
root.title("Sesión de Estudio")
root.geometry("400x400")

frame=ttk.Frame(root)
def elegir_carpeta(*args):
    carpeta=filedialog.askdirectory()
    
root.mainloop()