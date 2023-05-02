from pynput import keyboard
from src.game_learn import GameLearn

if __name__ == "__main__":
    # game learn
    game_learn = GameLearn(
        source_lang="french",
        target_lang="chinese"
    )
    # Start listening for key events
    with keyboard.Listener(on_press=game_learn.on_press) as listener:
        listener.join()