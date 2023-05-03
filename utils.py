import tkinter as tk

def push_image_to_front(image_path: str = None):
    """
    Push an image to the front of the screen.
    """
    # Create the main window
    root = tk.Tk()

    # Load the image and create a PhotoImage object
    image = tk.PhotoImage(file="./image/screenshot.png")

    # Create a label with the image and add it to the window
    label = tk.Label(root, image=image)
    label.pack()

    # Raise the label to the top of the window stack
    label.lift()

    # Start the main event loop
    root.mainloop()

push_image_to_front()