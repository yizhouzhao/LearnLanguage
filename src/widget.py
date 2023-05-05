import customtkinter
from PIL import Image

from .translate import translate
from .game_learn import Learner
import webbrowser

class NoteWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("240x300")
        self.title("Wold list")

        self.word_list = []
        self.word_translate_list = []
        self.text2button = {}
        

        # self.label = customtkinter.CTkLabel(self, text="Word list")
        # self.label.pack()

        self.frame = customtkinter.CTkScrollableFrame(master=self)
        self.frame.pack(fill="both", expand=True)

    def build_word_list(self, word_list:list):
        if len(word_list) > 0:
            self.word_list = word_list

            # translate if needed
            if len(self.word_translate_list) == 0:
                word_all = "\n".join(word_list)
                self.translate_word_list = translate(word_all, Learner.target_lang_code, Learner.source_lang_code).split("\n")
                assert len(self.translate_word_list) == len(self.word_list), "wrong translation"

            for idx, word in enumerate(word_list):
                self.build_block(word, self.translate_word_list[idx], idx)

            # self.build_block("Word 1", "Translation 1", 0)
            # self.build_block("Worsdffdsfsd 1", "Tran 1", 0)


    def write_word_to_file(self, word):
        with open("./data/notes.txt", "ab") as f:
            f.write(word)
        
        button = self.text2button[word]
        button.configure(state="disabled")
        
    def build_block(self, word:str, translation:str, index:int):
        block = customtkinter.CTkFrame(master=self.frame, corner_radius=10, fg_color="transparent") #  
        
        read_button = customtkinter.CTkButton(master=block, width = 20, text= " ", fg_color="#4aad34",
                                         command=lambda word = word: self.master.say_sentence(word)
        )
        read_button.grid(row = 0, column = 0, padx=2, sticky="w")
        
        word_label = customtkinter.CTkLabel(block, text=word)
        word_label.grid(row = 0, column = 1, padx=5, sticky="w")

        translation_label = customtkinter.CTkLabel(block, text=translation)
        translation_label.grid(row = 0, column = 2, padx=5)

        write_line = (word + " " + translation + "\n").encode('utf8')
        write_button = customtkinter.CTkButton(master=block, width = 20, text= "+", fg_color="#714285",
                                         command=lambda : self.write_word_to_file(write_line)
        )
        self.text2button[write_line] = write_button

        write_button.grid(row = 0, column = 3, padx=2, sticky="e")
        lookup_button = customtkinter.CTkButton(master=block, width = 20, text= "Collins", fg_color="#328afc",
                                         command=lambda : webbrowser.open(f'https://www.collinsdictionary.com/dictionary/{Learner.source_lang}-english/{word}'))
        lookup_button.grid(row = 0, column = 4, padx=2, sticky="e")

        add_button = customtkinter.CTkButton(master=block, width = 20, text= "Yaodao", fg_color="#991567",
                                         command=lambda : webbrowser.open(f'https://www.youdao.com/result?word={word}&lang={Learner.source_lang_code}'))
        add_button.grid(row = 0, column = 5, padx=2, sticky="e")
        
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
        self.label = customtkinter.CTkLabel(self, text= "Loading...", image=image)
        print("loading image size", image.cget("size"))
        self.label.pack(padx=0, pady=0)