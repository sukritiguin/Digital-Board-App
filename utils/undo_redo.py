from imports import *

class UndoRedo:
    def undo(self, event):
        if self.canvas.find_all():
                self.canvas.delete(self.canvas.find_all()[-1])

    def redo(self, event):
        pass


if __name__ == "__main__":
    pass