import tkinter as tk
import customtkinter
import os
from PIL import Image

import asyncio
import threading
import pyttsx3

from .widget import NoteWindow, LoadingWindow
from .utils import get_words_from_result


class AppUI(customtkinter.CTk):
    def __init__(self, window_size = (1920, 1080)):
        super().__init__()
        self.window_size = window_size

        self.title("Learn a new language.py")
        # self.window_size = (width, height)
        self.geometry(f"{self.window_size[0]}x{self.window_size[1]}")

        # create menu
        self.create_menu()
        self.wordlist_window = None
        self.word_list = []
        self.word_trans_list = []

        self.loading_window = None

        # create main part
        self.open_image()

        # init reading engine
        self.init_reading_engine()

    def create_menu(self):

        # Creating Menubar
        menubar = tk.Menu(self)
        
        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = file)
        # Add open word list
        file.add_command(label ='Open word list', command = self.open_wordlist, font=('Arial', 20))
        # Add open notebook
        file.add_command(label ='Open notebook', 
                         command = lambda : os.startfile(f"{os.path.dirname(os.path.realpath(__file__))}/../data/notes.txt"), 
                         font=('Arial', 20))
        self.config(menu = menubar)
    
    def open_wordlist(self):
        if self.wordlist_window is None or (not self.wordlist_window.winfo_exists()):
            self.wordlist_window = NoteWindow(self)  # create window if its None or destroyed
            # build word list
            self.wordlist_window.build_word_list(self.word_list)

            self.wordlist_window.after(10, self.wordlist_window.lift)
            print("creating new window")
        else:
            self.wordlist_window.focus()  # if window exists focus it
    
    def close_word_list(self):
        if self.wordlist_window is not None and self.wordlist_window.winfo_exists():
            self.wordlist_window.destroy()
            self.wordlist_window = None
    
    def open_loading(self):
        """
        Open Loading window
        """
        if self.loading_window is None or (not self.loading_window.winfo_exists()):
            self.loading_window = LoadingWindow(self)  # create window if its None or destroyed
            self.loading_window.after(1, self.loading_window.lift)
            print("creating loading window")
            self.loading_window.focus()  # if window exists focus it
            self.loading_window.lift()

    def close_loading(self):
        """
        Close Loading window
        """
        if self.loading_window is not None and self.loading_window.winfo_exists():
            self.loading_window.destroy()
            self.loading_window = None
    
    def open_image(self, image_path:str = "./src/ui_image/francais.PNG"):
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # # load images with light and dark mode image
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        # print("image_path", image_path)
        self.main_image = Image.open(image_path)
        self.main_image_size = self.main_image.size
        # image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        main_ctkimage = customtkinter.CTkImage(self.main_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        print("image size", self.winfo_screenwidth(), self.winfo_screenheight())

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame.grid_columnconfigure(0, weight=1)

        self.main_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=main_ctkimage)
        self.main_image_label.grid(row=0, column=0, padx=0, pady=0)

        # select default frame
        # self.select_frame_by_name("home")
        self.home_frame.pack() #grid(row=0, column=0, sticky="nsew")

    def update_image(self, image_path:str = "./image/screenshot.png", half_transparent = False):
        """
        update image in main image label
        """
        self.main_image = Image.open(image_path)
        if half_transparent:
            self.main_image.putalpha(127)

        self.main_image_size = self.main_image.size
        # new_image = new_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        main_ctkimage = customtkinter.CTkImage(self.main_image, size=(self.winfo_screenwidth() * 0.9, self.winfo_screenheight() * 0.9))
    
        self.main_image_label.configure(image = main_ctkimage)

    def add_sound_buttons(self, result):
        # clean result
        result = result[0]
        boxes = [line[0] for line in result]
        scores = [line[1][1] for line in result]
        txts = [line[1][0] for line in result]

        # scaler_x = self.winfo_screenwidth() / self.main_image_size[0] * 0.9
        # scaler_y = self.winfo_screenheight() / self.main_image_size[1] * 0.9
        # print("scaler", scaler_x, scaler_y, self.main_image_size)
        
        for i in range(len(boxes)):
            box = boxes[i]
            sound_button = customtkinter.CTkButton(master=self.home_frame, width = 8, height = 8, text= ' ', # txts[i]
                                            command=lambda i = i: self.say_sentence(txts[i]), # txts[i]
                                            font = ("Times", 8),
                                            fg_color="#4aad34",
                                            # bg_color="transparent",
                                            )
            # print(i, "box", box, box[0][0] * scaler_x, box[0][1] * scaler_y)
            # read_button.place(x = box[0][0] * scaler_x, y=box[0][1] * scaler_y, anchor="nw")
            sound_button.place(relx=box[0][0] / self.main_image_size[0] - 0.01, 
                              rely=box[0][1] / self.main_image_size[1], 
                              anchor="nw")
            # read_button.attributes("-alpha", 0.5)
            # read_button.attributes("-topmost", True)
            self.sound_buttons.append(sound_button)
    
    def delete_sound_buttons(self):
        for button in self.sound_buttons:
            button.destroy()
        
        self.sound_buttons.clear()
            

    ################################### ui functions ###################################
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update_word_list(self, result):
        """
        update word list from ocr result
        """
        self.word_list = get_words_from_result(result)
        # print("!!!!!!!!!!!!word_list!!!!!!!!!!", self.word_list)

    def reset_ui(self):
        self.close_word_list()
        self.delete_sound_buttons()

    ################################### reading engine ###################################
    def init_reading_engine(self):
        # init reading engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        from .game_learn import Learner
        lang_code = Learner.source_lang_code
        for voice in voices:
            if lang_code in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.is_reading = False
        self.sound_buttons = []

    def say_sentence(self, sentence):
        """
        Say sentence
        """
        # print("saying sentence: ", sentence)
        # self.engine.say(sentence)
        # self.engine.runAndWait()

        def read_word(word):
            if not self.is_reading:
                self.is_reading = True
                self.engine.say(word)
                self.engine.runAndWait()
                self.is_reading = False

        # Create a new thread to read the word
        thread = threading.Thread(target=read_word, args=(sentence,))
        thread.start()
        # thread.join()


if __name__ == "__main__":
    app_ui = AppUI()
    app_ui.after(0, lambda:app_ui.state('zoomed'))
    print("winfo_width() ", app_ui.winfo_screenheight(), app_ui.winfo_screenheight())
    app_ui.mainloop()