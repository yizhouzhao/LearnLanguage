import customtkinter
from PIL import Image

from .animate_gif import AnimatedGif

class NoteWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Notebook")
        self.label.pack(padx=20, pady=20)

class LoadingWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget_size = 100
        self.geometry(f"{widget_size}x{widget_size}")
        image_path:str = "./src/ui_image/loading.png"
        image = customtkinter.CTkImage(Image.open(image_path), size=(widget_size, widget_size))
        self.label = customtkinter.CTkLabel(self, text= "Analyzing...", image=image)
        print("loading image size", image.cget("size"))
        self.label.pack(padx=0, pady=0)