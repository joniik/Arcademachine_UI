import os
import customtkinter
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk
from pyjoystick.sdl2 import Joystick, Key, run_event_loop
import threading
import psutil 

arcadeBackground = "Background.mp4"
video_play_interval = 20000 



game_open = False

def add_joystick(joystick):
    print('Added', joystick)

def remove_joystick(joystick):
    print('Removed', joystick)

x = 0

def handle_key_event(key):
    global x
    
    if key.keytype == Key.AXIS:
        if key.number == 0:
            if game_open == False:
                if key.value == -1:
                    print("left")
                    print (game_open)
                    x = (x - 1) % len(image_list)
                elif key.value == 1:
                    print("right")
                    print (game_open)
                    x = (x + 1) % len(image_list)

    elif key.keytype == Key.BUTTON and key.number == 0:
        if key.value == 1:
            if game_open == False:
                print("play")
                open_files()



    
    update_display(x)

    

def create_thumbnail_image(image_path, size=(1100, 550), fallback_image_path="default_thumbnail.png"):
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
    create_thumbnail_image(os.path.join(os.path.dirname(folder_files[0]), "thumbnail.png"), fallback_image_path="default_thumbnail.png")
    for folder_files in folder_files_list
]

def open_files():
    global game_open  # Declare the variable as global

    current_folder_files = folder_files_list[x]
    for path in current_folder_files:
        os.startfile(path)

    # Set the game_open variable to True when the game is open
    game_open = True

def joystick_loop():
    run_event_loop(add_joystick=add_joystick, remove_joystick=remove_joystick, handle_key_event=handle_key_event)

def update_display(image_number):
    global x

    image_number %= len(image_list)
    x = image_number  # Update the current image index
    current_folder_files = folder_files_list[x]
    current_folder_name = os.path.basename(current_folder_files[0])

    my_label.configure(image=image_list[image_number])
    game_name_label.configure(text=current_folder_name)


def update_display_loop():
    update_display(x)
    app.after(1000, update_display_loop) 
    
 # Schedule the next update in 1 second

def tkinter_loop():
    customtkinter.set_appearance_mode("dark")
    global app, my_label, game_name_label,background_image

    app = customtkinter.CTk()

    app.wm_attributes('-transparentcolor', '#ab23ff')
    background_image = tk.PhotoImage(file="Gradient.png")


    # Load and display the video as the background
    video_canvas = TkinterVideo(master=app, anchor="center")
    video_canvas.load("Background.mp4")  # Replace with the path to your video file
    video_canvas.pack(fill="both", expand=True)  # Expand to fill the window
    video_canvas.play()
    

    my_label = customtkinter.CTkLabel(app, image=image_list[0], text="")
    my_label.place(relx=0.5, rely=0.53, anchor="center")


    game_name_label = customtkinter.CTkLabel(app, text="",text_color="white")
    game_name_label.place(relx=0.5, rely=0.925, anchor="s")
    game_name_label.configure(image=background_image)

    

    current_folder_name = os.path.basename(folder_files_list[0][0])
    game_name_label.configure(text=current_folder_name, font=("Arcade Normal", 25),)

    app.geometry("1920x1080")  # Set your desired window size here
    app.attributes("-fullscreen", "True")

    schedule_video_playback(video_canvas) 


    update_display_loop()  # Start the update display loop
    app.mainloop()


def schedule_video_playback(video_canvas):
    video_canvas.play()
    app.after(video_play_interval, schedule_video_playback, video_canvas)


def check_game_open():
    global game_open

    while True:
        if game_open:
            # Check if the game process is running by its executable name
            game_process_name = os.path.basename(folder_files_list[x][0])
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == game_process_name:
                    break
            else:
                # The game process is not running, so set game_open to False
                game_open = False

def main():
    joystick_thread = threading.Thread(target=joystick_loop)
    joystick_thread.start()

        # Start a thread to check if the game is open
    game_check_thread = threading.Thread(target=check_game_open)
    game_check_thread.start()

    tkinter_loop()

if __name__ == "__main__":
    main()
