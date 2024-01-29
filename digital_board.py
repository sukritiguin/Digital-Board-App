from imports import *
from initilizer import Initilizer

class DigitalBoard:
    def __init__(self, root):
        Initilizer.initilize(self=self, root=root)


def on_escape(event):
    result = messagebox.askyesno("Quit", "Do you want to quit the application?")
    if result:
        root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    
    root.attributes('-fullscreen', True)

    # Prevent the user from resizing the window
    root.resizable(False, False)

    # Load your custom icon image
    custom_icon = tk.PhotoImage(file="./images/notebook.png")  # Replace "your_custom_icon.png" with your icon file path

    # Set the custom icon
    root.iconphoto(False, custom_icon)

    # Bind the Escape key to the on_escape function
    root.bind("<Escape>", on_escape)

    app = DigitalBoard(root)
    root.mainloop()