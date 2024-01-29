from imports import *
from utils.create_canvas_props import CreateCanvas

class Initilizer:
    def initilize(definer=None, self=None, root=None):
        self.root = root
        self.root.title("Digital Board")
        self.style = Style(theme="flatly")
        
        self.background = "white"
        self.transparency = "rgba(0,0,0,0.01)"
        
        self.paste_image_x = None
        self.paste_image_y = None
        
        # self.canvas = tk.Canvas(root, bg=self.background, width=800, height=600)

        self.slides = []  # List to store canvas objects (slides)
        self.current_slide_index = 0  # Index of the currently displayed slide
        
        self.text_boxes = []
        self.text_color = "black"  # Default text color
        self.font = ("Arial", 12, "bold")  # Default font


        self.canvas_scale = 1.0  # Initial scale factor
        self.canvas_width = 800  # Initial canvas width
        self.canvas_height = 600  # Initial canvas height     

        self.selection_rect = None  # Rectangle for user selection
        self.clipboard = None  # Variable to store the copied selection
    

        CreateCanvas.create_canvas(self=self)
        self.canvas = self.slides[self.current_slide_index]
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        
        self.canvas_image = []
        
    
    
        
        self.pen_color = "black"
        self.pen_width = 2
        self.eraser_color = self.background
        self.eraser_width = 10
        self.shapes = []  # To store drawn shapes
        self.current_shape = None
        self.current_tool = "pen"
        self.is_drawing = False
        self.prev_x, self.prev_y = None, None  # Previous mouse coordinates for Bézier curves
        
        self.text_box = None  # To store the current text box
        self.text_color = "black"
        self.font = ("Arial", 12, "bold")
        
        self.recent_colors = ["red", "blue", "black"]
        CreateCanvas.create_toolbar(self=self)
        
            
        CreateCanvas.bind_events(self=self)