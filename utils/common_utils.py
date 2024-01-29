from .undo_redo import UndoRedo
from .save_canvas import SaveCanvas
from .create_drawing import Draw
from imports import *

def bind_events(definer=None, self=None):
    self.canvas.bind("<Button-1>", lambda event: Draw.start_drawing(self, event))
    self.canvas.bind("<B1-Motion>", lambda event: Draw.draw(self, event))
    self.canvas.bind("<ButtonRelease-1>", lambda event: Draw.stop_drawing(self, event))

    self.canvas.bind("<MouseWheel>", lambda event: zoom_with_mouse(self, event))  # Capture mouse scroll events

    self.canvas.bind("<Button-3>", lambda event: show_context_menu(self, event))

    self.root.bind("<Control-z>", lambda event: UndoRedo.undo(self, event))
    self.root.bind("<Control-y>", lambda event: UndoRedo.redo(self, event))

    # Creating meno to handing file options

    menubar = tk.Menu(self.root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save", command=SaveCanvas.save)
    file_menu.add_command(label="Open", command=SaveCanvas.open_file)
    menubar.add_cascade(label="File", menu=file_menu)
    self.root.config(menu=menubar)


    # Create a right-click context menu
    self.context_menu = Menu(self.canvas, tearoff=0)
    self.context_menu.add_command(label="Paste Image", command=paste_image)
    self.context_menu.add_command(label="Add Text", command=create_text_box)


if __name__ == "__main__":
    pass