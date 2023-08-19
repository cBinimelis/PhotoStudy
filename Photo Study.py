import tkinter as tk
import ttkbootstrap as ttk
import os, random, sys
from tkinter import *
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Emoji
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

#Obtener la ruta de la carpeta que se utilizará
def getfolderpath():
    global folderPath
    load_session_data()
    try:
        folder_selected = filedialog.askdirectory()
        folderPath=folder_selected
        llenarimg(image_time,session_time)
    except:
        print('Carpeta no seleccionada')

#Llenar la lista de imagenes
def llenarimg(t_img, t_ses):
    global list_img
    global total_img
    global load_progress
    total_img= int(t_ses/t_img)
    folder = folderPath
    load_progress = 0
    session_prog['maximum']=session_time
    load_prog['maximum']=total_img
    print(str(total_img))
    for x in range(total_img):
        file_path=folder + "\\" + random.choice(os.listdir(folder))
        img_path.append(file_path)
        img = Image.open(file_path)
        resized_img = resize(img, 595)
        x = ImageTk.PhotoImage(resized_img)
        list_img.append(x)
        load_progress += 1
        root.after(0, update_load)
        root.update()

#Funcion utilizada para actualizar la barrra de carga de imagenes en segundo plano
def update_load():
    if load_progress <= total_img:
        load_prog['value'] = load_progress

#Funcion utilizada para añadir una imagen extra a la lista
def agregar_extra(img_e):
    global total_img
    global list_img
    global cancel_id
    global image_progress
    file_path=folderPath + "\\" + random.choice(os.listdir(folderPath))
    img_path.append(file_path)
    img = Image.open(file_path)
    resized_img = resize(img, 595)
    x = ImageTk.PhotoImage(resized_img)
    list_img.append(x)
    image_progress = 0
    total_img = total_img + 1
    cancel_id = root.after(0,forward,img_e+1)
    print(str(cancel_id))

#Desde esta funcion se llama al timer de imagenes, está hecho de esta manera para evitar crear un loop,
#ya que de usar uno, no hay manera de controlar los ticks de actualización a voluntad
def image_timer():
    global session_progress
    global cancel_id
    i_t= image_time
    if session_progress < session_time:
        image_prog['maximum']=i_t
        if image_progress < i_t:
            root.after(0, update_timer)
    else:
        times_up()

#Funcion de timer central, acá se le toma el tiempo de la sesión y el tiempo individual de las imagenes
def update_timer():
    global session_progress
    global image_progress
    global update_cancel_id
    i_t = image_time
    if image_progress < i_t:
        if session_progress == session_time:
            session_progress=99999
            root.after_idle(times_up)
        elif session_progress < session_time:
            session_progress += 1
            image_progress += 1
            image_prog['value']=image_progress
            session_prog['value']=session_progress
            root.update()
            update_cancel_id=root.after(1000,update_timer)
        elif session_progress >= session_time:
            root.after_idle(times_up)
    else:
        if session_progress < session_time:
            image_progress=0
            forward(current_img+1)
            image_timer()
        else:
            times_up()

#Avanzar una imagen
def forward(img):
    global label
    global btn_forward
    global btn_back
    global current_img
    label.grid_forget()

    current_img=img    
    label = ttk.Label(viewer_frame, image=list_img[img - 1])
    label.bind("<Button-1>",lambda x=None: mostrar_imagen(img -1))
    btn_forward = ttk.Button(button_frame, text="Siguiente", command=lambda: agregar_extra(img))
    btn_back = ttk.Button(button_frame, text="Anterior", command=lambda: back(img-1))

    if current_img == total_img:
        btn_forward = ttk.Button(button_frame, text="Siguiente", state=DISABLED)
    if current_img == 1:
        btn_back = ttk.Button(button_frame, text="Anterior", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    btn_back.grid(column=0, row=0, sticky=NSEW)
    btn_forward.grid(column=2, row=0, sticky=NSEW)

#Retroceder una imagen
def back(img):
    global label
    global btn_forward
    global btn_back
    global current_img
    global image_progress
    label.grid_forget()

    current_img=img
    image_progress = 0
    label = ttk.Label(viewer_frame, image=list_img[img - 1])
    label.bind("<Button-1>",lambda x=None: mostrar_imagen(img -1))
    btn_forward = ttk.Button(
        button_frame, text="Siguiente", command=lambda: forward(img+1)
    )
    btn_back = ttk.Button(button_frame, text="Anterior", command=lambda: back(img-1))

    if current_img == 1:
        btn_back = ttk.Button(button_frame, text="Anterior", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    btn_back.grid(column=0, row=0, sticky=NSEW)
    btn_forward.grid(column=2, row=0, sticky=NSEW)

#Revisar si hay una carpeta seleccionada, en caso de que no sea asi, se exigirá una
def check():
    global list_img
    if not list_img:
        messagebox.showinfo(
            message="Aún no has seleccionado una carpeta con imágenes. Selecciona tu carpeta favorita y empezaremos con la sesión.",
            title="Carpeta no seleccionada",
        )
        getfolderpath()
    else:
        classes_in_session()

#Funcion para iniciar la sesion de estudio
def classes_in_session():
    global current_img
    global stop_button
    folder_button['state']=DISABLED
    combo_it['state']=DISABLED
    combo_st['state']=DISABLED
    btn_exit.grid_forget()
    stop_button = ttk.Button(f_frame, text=Emoji.get('Black Square for Stop'), bootstyle=DANGER, command=lambda: stop_session())

    stop_button.grid(column=6, row=0)
    button_frame.columnconfigure(1, weight=0)
    load_session_data()
    forward(1)
    image_timer()

#Funcion final, se llama cuando la sesión termina
def times_up():
    global session_progress
    global image_progress
    global load_progress
    global load_prog
    global list_img

    print('Seacabó')

    ask_retry = messagebox.askyesno(message='Sesión Finalizada, felicidades por su gran trabajo \n' + '¿Desea empezar de nuevo?', title='¡Se logró!')
    if ask_retry:
        session_progress=0
        image_progress=0
        load_progress=0
        list_img.clear()
        llenarimg(image_time,session_time)
        print('pos se repite')
        check()
    else:
        try:
            root.after_cancel(cancel_id)
        except:
            print('Sin ID para eliminar')
        going_nuclear()
         
def stop_session():
    ask=messagebox.askyesno(message='¿Desea finalizar la sesión de manera anticipada?', title='¿Alguna emergencia?')
    if ask:
        root.after_cancel(update_cancel_id)
        going_nuclear()

#Resetear la interfaz
def going_nuclear():
    global folderPath
    global stop_button
    global session_progress
    global image_progress
    global load_progress
    global load_prog
    global list_img
    global label
    global og_img1
    
    folderPath=''
    session_progress=0
    image_progress=0
    load_progress=0

    session_prog['value']=0
    image_prog['value']=0
    load_prog['value']=0

    list_img.clear()
    folder_button['state']=READONLY
    combo_it['state']=READONLY
    combo_st['state']=READONLY
    
    
    stop_button.grid_forget()

    btn_back = ttk.Button(button_frame, text="Anterior", command="back", state=DISABLED)
    btn_exit = ttk.Button(button_frame, text=Emoji.get("Eject Symbol"), bootstyle=DANGER, command=root.quit)
    btn_forward = ttk.Button(button_frame, text=Emoji.get("black right-pointing triangle"),command=lambda: check())

    button_frame.grid(column=0, row=3, sticky=(S, E, W))
    btn_back.grid_forget()
    btn_exit.grid(column=0, row=0, sticky=NSEW)
    btn_forward.grid(column=1, row=0, columnspan=4, sticky=NSEW)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    label = ttk.Label(viewer_frame, image=og_img1)
    label.grid(row=0, column=0, sticky=S + N)

# funcion para cambiar el tamaño de la imagen manteniendo la relacion de aspecto
def resize(im, new_width):
    width, height = im.size
    ratio = height / width
    new_height = int(ratio * new_width)
    resized_image = im.resize((new_width, new_height))
    return resized_image


# funcion para iniciar la sesión de estudio
def load_session_data():
    global image_time
    global session_time

    # Configurar tiempo para la transición de imágenes
    if combo_it.current() == 0:
        messagebox.showwarning(
            message="No puedes iniciar una sesión sin seleccionar la duración de las imágenes",
            title="Tiempo desconfigurado",
        )
    elif combo_it.current() == 1:
        image_time = 30
    elif combo_it.current() == 2:
        image_time = 60
    elif combo_it.current() == 3:
        image_time = 120
    elif combo_it.current() == 4:
        image_time = 300
    elif combo_it.current() == 5:
        image_time = 600

    # Configurar tiempo total de la sesión de estudio
    if combo_st.current() == 0:
        messagebox.showwarning(
            message="No puedes iniciar una sesión sin seleccionar la duración que tendrá",
            title="Tiempo desconfigurado",
        )
    elif combo_st.current() == 1:
        session_time = 600
    elif combo_st.current() == 2:
        session_time = 1200
    elif combo_st.current() == 3:
        session_time = 1800
    elif combo_st.current() == 4:
        session_time = 3600
    elif combo_st.current() == 5:
        session_time = 7200

def mostrar_imagen(id):
    Image.open(img_path[id]).show()


basedir = os.path.dirname(__file__)
try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

root = ttk.Window(themename="superhero")
root.title("Photo Study")
root.iconbitmap(os.path.join(basedir, "logo.ico"))
root.resizable(False,False)
root.maxsize(600, 950)
root.minsize(600, 600)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
# root.attributes('-topmost',1)

folderPath = tk.StringVar()
list_img = list()
img_path = list()
image_time = int()
session_time = int()
session_progress= int()
image_progress= int()
load_progress= int()
total_img = int()
current_img = int()
og_img1=ImageTk
cancel_id = None
update_cancel_id = None

top_frame = ttk.Frame(root, height=950, width=600)

f_frame = ttk.Frame(top_frame)
folder_button = ttk.Button(f_frame, text=Emoji.get("File Folder"), command=lambda: getfolderpath())

image_frame = ttk.Frame(top_frame, borderwidth=1, height=800, width=600)
image_frame.grid_propagate(False)
viewer_frame = ttk.Frame(image_frame)
og_img1 = ImageTk.PhotoImage(Image.open(os.path.join(basedir,"demo.jpg")))
label = ttk.Label(viewer_frame, image=og_img1)

# Botones de seleccion de imagen
button_frame = ttk.Frame(top_frame, borderwidth=1)
btn_back = ttk.Button(button_frame, text="Anterior", command="back", state=DISABLED)
btn_exit = ttk.Button(button_frame, text=Emoji.get("Eject Symbol"), bootstyle=DANGER, command=root.quit)
btn_forward = ttk.Button(button_frame, text=Emoji.get("black right-pointing triangle"),command=lambda: check())

# Botones de seleccion de tiempo
time_frame = ttk.LabelFrame(top_frame, text="Seleccion de tiempos", borderwidth=1)
combo_it = ttk.Combobox(
    time_frame,
    state="readonly",
    values=["Duracion de cada imagen...", "30 Seg", "1 Min", "2 Min", "5 Min", "10 Min"],
    bootstyle=SECONDARY)
combo_st = ttk.Combobox(
    time_frame,
    state="readonly",
    values=["Duración de la sesión...", "10 Min", "20 Min", "30 Min", "1 Hrs", "2 Hrs"],
    bootstyle=SECONDARY)
load_prog = ttk.Progressbar(time_frame, length=total_img, value=0, bootstyle=SUCCESS)
image_prog = ttk.Progressbar(time_frame, length=total_img, value=0)
session_prog = ttk.Progressbar(time_frame, length=total_img, value=0, bootstyle=INFO)

# ----------------------------------------POSICIONAMIENTO----------------------------------------#
# Posición contenedor principal
top_frame.grid(column=0, row=0, sticky=NSEW)

# Posicion boton para seleccionar carpeta
f_frame.grid(column=0, row=1, sticky=NSEW)
folder_button.grid(column=0, row=0,columnspan=6 , sticky=NSEW)

f_frame.columnconfigure(0, weight=5)

# Posicion visor de imagenes
image_frame.grid(column=0, row=2, sticky=S + N)
viewer_frame.grid(column=0, row=0, sticky=S + N)
label.grid(row=0, column=0, sticky=S + N)

# Posicion botones inferiores
button_frame.grid(column=0, row=3, sticky=(S, E, W))
# btn_back.grid(column=0,row=0, sticky=NSEW)
btn_exit.grid(column=0, row=0, sticky=NSEW)
btn_forward.grid(column=1, row=0, columnspan=4, sticky=NSEW)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

# Seleccion de tiempo
time_frame.grid(column=0, row=4, sticky=NSEW)
combo_it.grid(column=0, row=0, sticky=NSEW)
combo_it.current(1)
combo_st.grid(column=1, row=0, sticky=NSEW)
combo_st.current(1)

image_prog.grid(column=0, row=1, columnspan=2, sticky=EW)
session_prog.grid(column=0, row=2, columnspan=2, sticky=EW)
load_prog.grid(column=0, row=3,columnspan=2, sticky=NSEW)

time_frame.columnconfigure(0,weight=1)
time_frame.columnconfigure(1,weight=1)



root.mainloop()
