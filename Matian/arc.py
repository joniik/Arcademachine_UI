import os
from tkinter import *
import customtkinter
from PIL import Image

def open_file(file_path):
    os.startfile(file_path)

def create_thumbnail_image(image_path, size=(30, 30)):
    return customtkinter.CTkImage(dark_image=Image.open(image_path), size=size)

def create_button_with_thumbnail(parent, folder_files, thumbnail_image):
    button = customtkinter.CTkButton(parent, text="Play", command=lambda: [open_file(path) for path in folder_files])
    customtkinter.CTkLabel(parent, text="", image=thumbnail_image, fg_color="transparent").grid(row=x, column=2, padx=25, pady=25)
    button.grid(row=x, column=1, padx=25, pady=25)
    return button

customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()

folder_list = set()
for folder_path, _, files in os.walk("Pelit"):
    for file in files:
        if file.endswith(".txt"):
            folder_list.add(os.path.basename(folder_path))

print(folder_list)

image_list = []
x = 0
for folder_name in folder_list:
    folder_path = os.path.join("Pelit", folder_name)
    folder_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".txt")]
    thumbnail_path = os.path.join(folder_path, "thumbnail.jpg")
    thumbnail_image = create_thumbnail_image(thumbnail_path)
    image_list.append(thumbnail_image)
    
    customtkinter.CTkLabel(app, text=folder_name).grid(row=x, column=0)
    create_button_with_thumbnail(app, folder_files, thumbnail_image)
    
    x += 1

app.attributes("-fullscreen", True)
app.mainloop()
