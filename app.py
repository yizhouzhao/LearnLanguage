from pynput import keyboard
from src.game_learn import Learner
from src.ui import AppUI
from src.utils import get_screen_size

class LearnApp:
    def __init__(self):
        # properties
        self.is_loading = True

        # start learner
        self.learner = Learner(
            source_lang="french",
            target_lang="chinese"
        )

        # add listener
        listener = keyboard.Listener(
            on_release=self.on_release
        )
        listener.start()
    

        # start ui
        self.ui = AppUI(window_size=get_screen_size())
        self.ui.after(0, lambda:self.ui.state('zoomed'))
        # self.ui.attributes('-alpha',0.5)
        self.ui.lift()
        # self.ui.attributes("-topmost", True)
        # self.ui.after(1, lambda:self.ui.lift())
        # start loop
        self.is_loading = False
        self.ui.mainloop()

    def on_release(self, key):
        # print("key pressed", key)
        if not self.is_loading:
            if key == keyboard.Key.print_screen:
                self.is_loading = True
                
                # Capture a screenshot
                self.learner.get_screenshot()
                self.ui.update_image(self.learner.image_path)
                self.ui.open_loading()

                # test button
                self.ui.add_sound_buttons()

                # # Perform OCR
                # result = self.learner.perform_ocr()
                # # update ui word list
                # self.ui.update_word_list(result)

                # # Perform translation and draw
                # image, image_path = self.learner.draw_ocr(result)

                # # Update image
                # self.ui.update_image(image_path)
                # self.ui.close_loading()
                # self.ui.lift()


            elif key == keyboard.Key.pause:
                exit()
            
            # unblock
            self.is_loading = False




if __name__ == "__main__":
    # # game learn
    # game_learn = GameLearn(
    #     source_lang="french",
    #     target_lang="chinese"
    # )
    # Start listening for key events
    # with keyboard.Listener(on_press=game_learn.on_press) as listener:
    #     listener.join()
    app = LearnApp()
    
