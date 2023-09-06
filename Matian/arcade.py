import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from pyjoystick.sdl2 import Joystick, Key, run_event_loop
import threading

arcadeBackground = "Pink.png"

def add_joystick(joystick):
    print('Added', joystick)

def remove_joystick(joystick):
    print('Removed', joystick)

x = 0

def handle_key_event(key):
    global x
    
    if key.keytype == Key.AXIS:
        if key.number == 0:
            if key.value == -1:
                print("left")
                x = (x - 1) % len(image_list)
            elif key.value == 1:
                print("right")
                x = (x + 1) % len(image_list)

    elif key.keytype == Key.BUTTON and key.number == 0:
        if key.value == 1:
            print("play")
            open_files()
    
    update_display(x)


def create_thumbnail_image(image_path, size=(1000, 700), fallback_image_path="default_thumbnail.jpg"):
    try:
        return customtkinter.CTkImage(dark_image=Image.open(image_path), size=size)
    except FileNotFoundError:
        return customtkinter.CTkImage(dark_image=Image.open(fallback_image_path), size=size)

folder_files_list = []
for folder_path, _, files in os.walk("Pelit"):
    exe_files = [
        os.path.join(folder_path, file)
        for file in files
        if file.endswith(".exe") and not file.lower().startswith("unitycrashhandler")
    ]
    if exe_files:
        folder_files_list.append(exe_files)

image_list = [
    create_thumbnail_image(os.path.join(os.path.dirname(folder_files[0]), "thumbnail.jpg"), fallback_image_path="default_thumbnail.jpg")
    for folder_files in folder_files_list
]

def open_files():
    current_folder_files = folder_files_list[x]
    for path in current_folder_files:
        os.startfile(path)

def joystick_loop():
    run_event_loop(add_joystick=add_joystick, remove_joystick=remove_joystick, handle_key_event=handle_key_event)

def update_display(image_number):
    global my_label, x

    my_label.grid_forget()

    image_number %= len(image_list)
    x = image_number  # Update the current image index
    current_folder_files = folder_files_list[x]
    current_folder_name = os.path.basename(current_folder_files[0])

    my_label = customtkinter.CTkLabel(app, image=image_list[image_number], text="")
    my_label.pack(expand=True, fill='both')
    game_name_label.configure(text=current_folder_name)

    my_label.place(relx=0.5, rely=0.05, anchor="n")

def tkinter_loop():
    customtkinter.set_appearance_mode("dark")
    global app, my_label, game_name_label

    app = customtkinter.CTk()

    my_label = customtkinter.CTkLabel(app, image=image_list[0], text="")
    my_label.place(relx=0.5, rely=0.05, anchor="n")

    game_name_label = customtkinter.CTkLabel(app, text="", fg_color="transparent")
    game_name_label.place(relx=0.5, rely=0.75, anchor="s")

    current_folder_name = os.path.basename(folder_files_list[0][0])
    game_name_label.configure(text=current_folder_name, font=("Aerial", 25))

    app.geometry("1920x1080")

    app.mainloop()

def main():
    joystick_thread = threading.Thread(target=joystick_loop)
    joystick_thread.start()

    tkinter_loop()

if __name__ == "__main__":
    main()
