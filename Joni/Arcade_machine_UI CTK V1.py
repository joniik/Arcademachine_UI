import os
import customtkinter
import tkinter
from CTkListbox import *

# Theme
customtkinter.set_appearance_mode("Dark")
# Color to Widgets
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()


# define app Name and Window Resolution
app.title("Testi")
app.geometry("1920x1080")

# Show value Function
def show_value(selected_option):
    print(selected_option)
    launch_game(selected_option)

# Launch Game Function
def launch_game(game_name):
    exe_file = f"{game_name}.exe"
    if os.path.exists(exe_file):
        os.system(exe_file)
    else:
        print(f"Executable '{exe_file}' not found!")


# List Box Object
listbox = CTkListbox(app, command=show_value)
listbox.pack(fill="both", expand=True, padx=400, pady=200)

script_directory = os.path.dirname(os.path.abspath(__file__))
executable_files = []

# Scanning for .exe files in the directory and adding them to the listbox
for file_name in os.listdir(script_directory):
    if file_name.endswith(".exe"):
        game_name = os.path.splitext(file_name)[0]
        listbox.insert("end", game_name)
        executable_files.append(game_name)
def browse_file():
    global executable_files
    root_dir = tkinter.filedialog.askdirectory()
    executable_files = get_executable_files(root_dir)
    listbox.delete(0, "end")
    for game_name in executable_files:
        listbox.insert("end", game_name)

#Button Object 
button = customtkinter.CTkButton(master=app, text="Pelaa", command=browse_file)
button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

# Scans Exe FiLes
def get_executable_files(root_dir):
    executable_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".exe"):
                game_name = os.path.splitext(file)[0]
                executable_files.append(game_name)
    return executable_files

#FullScreen
app.attributes("-fullscreen", "True")
# Runs the app
app.mainloop()
