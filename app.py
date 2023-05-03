from pynput import keyboard
from src.game_learn import Learner
from src.ui import AppUI
from src.utils import get_screen_size

class LearnApp:
    def __init__(self):
        # start ui
        self.ui = AppUI(window_size=get_screen_size())
        self.ui.after(0, lambda:self.ui.state('zoomed'))
        self.ui.mainloop()

        # start learner
        self.learner = Learner(
            source_lang="french",
            target_lang="chinese"
        )


if __name__ == "__main__":
    # # game learn
    # game_learn = GameLearn(
    #     source_lang="french",
    #     target_lang="chinese"
    # )
    # # Start listening for key events
    # with keyboard.Listener(on_press=game_learn.on_press) as listener:
    #     listener.join()
    app = LearnApp()
