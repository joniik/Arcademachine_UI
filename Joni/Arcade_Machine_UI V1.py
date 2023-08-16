import os
import tkinter as tk
from tkinter import filedialog
from subprocess import Popen

class AppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Avaa Peli")

        self.label = tk.Label(root, text="Valitse Peli:")
        self.label.pack()

        self.launch_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=150)
        self.launch_listbox.pack()

        self.browse_button = tk.Button(root, text="Etsi", command=self.browse_file)
        self.browse_button.pack()

        self.launch_button = tk.Button(root, text="Käynnistä", command=self.launch_selected)
        self.launch_button.pack()

        self.file_path = ""

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])

    def launch_selected(self):
        selected_index = self.launch_listbox.curselection()
        if selected_index:
            selected_item = self.launch_listbox.get(selected_index)
            Popen([selected_item])

def get_executable_files(root_dir):
    executable_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".exe"):
                executable_files.append(os.path.join(root, file))
    return executable_files

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)

    script_directory = os.path.dirname(os.path.abspath(__file__))
    game_folders = [f for f in os.listdir(script_directory) if os.path.isdir(os.path.join(script_directory, f))]

    executable_files = []
    for folder in game_folders:
        folder_path = os.path.join(script_directory, folder)
        executable_files.extend(get_executable_files(folder_path))

    for exe_file in executable_files:
        app.launch_listbox.insert(tk.END, exe_file)

    root.mainloop()
