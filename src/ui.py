import tkinter as tk

import customtkinter
import os
from PIL import Image

from .note import NoteWindow


class AppUI(customtkinter.CTk):
    def __init__(self, window_size = (1920, 1080)):
        super().__init__()
        self.window_size = window_size

        self.title("Learn a new language.py")
        # self.window_size = (width, height)
        self.geometry(f"{self.window_size[0]}x{self.window_size[1]}")

        # create menu
        self.create_menu()
        self.note_window = None

        # create main part
        self.open_image()

    def create_menu(self):

        # Creating Menubar
        menubar = tk.Menu(self)
        
        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = file)
        file.add_command(label ='Open note', command = self.open_notebook, font=('Arial', 20))

        self.config(menu = menubar)
    
    def open_notebook(self):
        if self.note_window is None or (not self.note_window.winfo_exists()):
            self.note_window = NoteWindow(self)  # create window if its None or destroyed
            self.note_window.after(10, self.note_window.lift)
            print("creating new window")
        else:
            self.note_window.focus()  # if window exists focus it
    
    def open_image(self, image_path:str = "./src/ui_image/loading.jpg"):
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # # load images with light and dark mode image
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        # print("image_path", image_path)
        image = Image.open(image_path)
        # image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        main_image = customtkinter.CTkImage(image, size=(self.winfo_screenwidth() * 0.9, self.winfo_screenheight() * 0.9))
        print("image size", main_image.cget("size"))

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame.grid_columnconfigure(0, weight=1)

        self.main_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=main_image)
        self.main_image_label.grid(row=0, column=0, padx=0, pady=0)

        # select default frame
        # self.select_frame_by_name("home")
        self.home_frame.pack() #grid(row=0, column=0, sticky="nsew")

    def update_image(self, image_path:str = "./image/screenshot.png"):
        """
        update image in main image label
        """
        new_image = Image.open(image_path)
        # new_image = new_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        new_image = customtkinter.CTkImage(new_image, size=(self.winfo_screenwidth() * 0.9, self.winfo_screenheight() * 0.9))
    
        self.main_image_label.configure(image = new_image)
        

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app_ui = AppUI()
    app_ui.after(0, lambda:app_ui.state('zoomed'))
    print("winfo_width() ", app_ui.winfo_screenheight(), app_ui.winfo_screenheight())
    app_ui.mainloop()