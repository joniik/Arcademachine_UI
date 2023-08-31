import os
import customtkinter
from tkinter import *
from PIL import Image
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from functools import partial
          
def activate_button_forward(event):
    button_forward.invoke()

def activate_button_back(event):
    button_back.invoke()

def activate_button_play(event):
    button_play.invoke()
    
def key_received(key):
    print('received', key)
    if key.value == Key.HAT_LEFT:
         button_back.invoke()
    elif key.value == Key.HAT_RIGHT:
        button_forward.invoke()

def create_thumbnail_image(image_path, size=(1000, 700), fallback_image_path="default_thumbnail.jpg"):
    try:
        return customtkinter.CTkImage(dark_image=Image.open(image_path), size=size)
    except FileNotFoundError:
        return customtkinter.CTkImage(dark_image=Image.open(fallback_image_path), size=size)


def update_display(image_number):
    global my_label, button_back, button_forward, current_folder_files, current_folder_name, game_name_label

    my_label.grid_forget()

    image_number %= len(image_list)
    current_folder_files = folder_files_list[image_number]
    current_folder_name = os.path.basename(current_folder_files[0])

    my_label = customtkinter.CTkLabel(app, image=image_list[image_number], text="")
    my_label.pack(expand=True, fill='both')
    game_name_label.configure(text=current_folder_name)
    button_back.configure(command=partial(update_display, image_number - 1))
    button_forward.configure(command=partial(update_display, image_number + 1))

    my_label.place(relx = 0.5, rely = 0.05, anchor = N)

def open_files():
    for path in current_folder_files:
        os.startfile(path)

customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()

app.bind("<d>", activate_button_forward)
app.bind("<a>", activate_button_back)
app.bind("<space>", activate_button_play)

def print_add(joy):
    print('Added', joy)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    if key.value == Key.HAT_LEFT:
        activate_button_back
    elif key.value == Key.HAT_RIGHT:
        activate_button_forward

folder_files_list = []
for folder_path, _, files in os.walk("Pelit"):
    exe_files = [
        os.path.join(folder_path, file)
        for file in files
        if file.endswith(".exe") and not file.lower().startswith("UnityCrashHandler")
    ]
    if exe_files:
        folder_files_list.append(exe_files)

image_list = []
for folder_files in folder_files_list:
    thumbnail_path = os.path.join(os.path.dirname(folder_files[0]), "thumbnail.jpg")
    thumbnail_image = create_thumbnail_image(thumbnail_path, fallback_image_path="default_thumbnail.jpg")
    image_list.append(thumbnail_image)

my_label = customtkinter.CTkLabel(app, image=image_list[0], text="") 
my_label.place(relx = 0.5, rely = 0.05, anchor = N)

game_name_label = customtkinter.CTkLabel(app, text="", fg_color="transparent")
game_name_label.place(relx = 0.5, rely = 0.75, anchor = S)


button_back = customtkinter.CTkButton(app, text="<<")
button_play = customtkinter.CTkButton(app, text="Play", command=open_files)
button_forward = customtkinter.CTkButton(app, text=">>")

#Nappi Paikat
button_back.place(relx = 0.4, rely = 0.8, anchor = S)
button_play.place(relx = 0.5, rely = 0.8, anchor = S)
button_forward.place(relx = 0.6, rely = 0.8, anchor = S)

current_folder_name = os.path.basename(folder_files_list[0][0])
game_name_label.configure(text=current_folder_name, font=("Aerial", 25) )

button_back.configure(command=partial(update_display, len(image_list) - 1))
button_forward.configure(command=partial(update_display, 1))


#app.attributes("-fullscreen", True)
app.mainloop(print_add, print_remove, key_received)