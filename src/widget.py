import customtkinter
from PIL import Image

from .animate_gif import AnimatedGif

class NoteWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("240x300")
        self.title("Wold list")

        # self.label = customtkinter.CTkLabel(self, text="Word list")
        # self.label.pack()

        self.frame = customtkinter.CTkScrollableFrame(master=self)
        self.frame.pack(fill="both", expand=True)

        self.build_block("Word 1", "Translation 1", 0)
        self.build_block("Worsdffdsfsd 1", "Tran 1", 0)
        
    def build_block(self, word:str, translation:str, index:int):
        block = customtkinter.CTkFrame(master=self.frame, corner_radius=10, fg_color="transparent") #  
        button = customtkinter.CTkButton(master=block, width = 20, text= "D", command=None)
        button.grid(row = 0, column = 0, padx=5, sticky="w")
        word_label = customtkinter.CTkLabel(block, text=word)
        word_label.grid(row = 0, column = 1, padx=5)
        translation_label = customtkinter.CTkLabel(block, text=translation)
        translation_label.grid(row = 0, column = 2, padx=5, sticky="e")
        
        block.grid(sticky = "nw", pady = 3)

        # word_label2 = customtkinter.CTkLabel(self.frame, text="Word 2")
        # word_label2.grid(row = 1, column = 0, padx=10, pady=10)
        # button_2 = customtkinter.CTkButton(master=self.frame, width = 20, text= "D", command=None)
        # button_2.grid(row = 1, column = 1, padx=10, pady=10, sticky="e")

       
        

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