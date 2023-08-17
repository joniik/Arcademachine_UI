from tkinter import *
from tkinter import ttk
import os

def open_file(file_path):
    os.startfile(file_path)

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()

file_list = []
for folder_path, _, files in os.walk("Pelit"):
    for file in files:
        if file.endswith(".txt"):
            file_list.append(os.path.join(folder_path, file))

print(file_list)

x = 0
print(len(file_list))
for file_path in file_list:
    ttk.Label(frm, text=file_path).grid(column=0, row=x)
    ttk.Button(frm, text="Play", command=lambda path=file_path: open_file(path)).grid(column=1, row=x)
    x += 1

root.mainloop()
