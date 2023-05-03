import tkinter as tk

import customtkinter
import os
from PIL import Image

from note import NoteWindow


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Learn a new language.py")
        # self.window_size = (width, height)
        self.geometry("1920x1080")

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
    
    def open_image(self):
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        print("image_path", image_path)
        image = Image.open(os.path.join(image_path, "../../image/screenshot.png"))
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.large_test_image = customtkinter.CTkImage(image, size=(self.winfo_screenwidth() * 0.9, self.winfo_screenheight() * 0.9))
        print("image size", self.large_test_image.cget("size"))

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=0, pady=10)

        # select default frame
        # self.select_frame_by_name("home")
        self.home_frame.pack() #grid(row=0, column=0, sticky="nsew")

        

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.after(0, lambda:app.state('zoomed'))
    print("winfo_width() ", app.winfo_screenheight(), app.winfo_screenheight())
    app.mainloop()