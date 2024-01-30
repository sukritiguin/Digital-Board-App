from imports import *
from .setup import Setup
from .undo_redo import UndoRedo
from .save_canvas import SaveCanvas, LoadShapes
from .create_drawing import Draw, SetColor


def destroy_canvas(self):
    # Display a warning message before destroying the canvas
    response = messagebox.askokcancel("Confirmation", "Are you sure you want to destroy the canvas?")
    if response:
        self.root.destroy()
        messagebox.showinfo("Info", "Canvas destroyed successfully!")

class CreateCanvas:

    def create_canvas(definer=None, self=None):
        canvas = tk.Canvas(self.root, bg=self.background, width=self.canvas_width, height=self.canvas_height)  # Set the initial dimensions
        canvas.pack(fill=tk.BOTH, expand=True)
        self.slides.append(canvas)



    def create_toolbar(definer=None, self=None):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        
        pen_image = Image.open("./images/pen.png")  # Replace with the path to your pen icon image
        pen_image = pen_image.resize((32, 32), Image.ANTIALIAS)
        pen_icon = ImageTk.PhotoImage(pen_image)
        pen_button = ttk.Button(toolbar, image=pen_icon, command=lambda: Draw.set_tool(self, "pen"))
        pen_button.image = pen_icon
        pen_button.pack(side=tk.LEFT, padx=5)
        
        pen_size_slider = ttk.Scale(toolbar, from_=2, to=20, orient="horizontal", length=100, command=lambda value: Draw.set_pen_size(self, value))
        pen_size_slider.set(self.pen_width)
        pen_size_slider.pack(side=tk.LEFT, padx=5)
        
        eraser_image = Image.open("./images/eraser.jpg")  # Replace with the path to your eraser icon image
        eraser_image = eraser_image.resize((32, 32), Image.ANTIALIAS)
        eraser_icon = ImageTk.PhotoImage(eraser_image)
        eraser_button = ttk.Button(toolbar, image=eraser_icon, command=lambda: Draw.set_tool(self, "eraser"))
        eraser_button.image = eraser_icon
        eraser_button.pack(side=tk.LEFT, padx=5)
        
        eraser_size_slider = ttk.Scale(toolbar, from_=20, to=100, orient="horizontal", length=100, command=lambda value: Draw.set_eraser_size(self, value))
        eraser_size_slider.set(self.eraser_width)
        eraser_size_slider.pack(side=tk.LEFT, padx=5)
        
        self.recent_color_buttons = []
        for i, recent_color in enumerate(self.recent_colors):
            style = Style()
            style.configure(recent_color + ".TButton", background=recent_color, foreground=recent_color)
            recent_color_button = ttk.Button(toolbar, text="", width=2, style=recent_color + ".TButton",
                                            command=lambda color=recent_color, index=i: SetColor.set_recent_color(self, color, index))
            recent_color_button.pack(side=tk.LEFT, padx=2)
            self.recent_color_buttons.append(recent_color_button)
            
            # Bind right mouse click to change color of the specific button
            recent_color_button.bind("<Button-3>", lambda event, color=recent_color, index=i: Draw.change_color_right_click(self, index))

        # Shapes section
        shapes_frame = ttk.Frame(toolbar)
        shapes_frame.pack(side=tk.LEFT, padx=20)

        shape_icons = [
            "./rectangle.webp",
            "./circle.png",
            "./square.webp",
            "./line.jpg",
            "./arrow.png",
            "./arrow-2faced.png",
            "./triangle.png",
        ]
        
        self.shape_icons_dict = {
            # "rectangle": "./rectangle.webp",
            "circle": "./images/circle.png",
            "square": "./images/rectangle.png",
            "line": "./images/line.jpg",
            "arrow": "./images/arrow.png",
            "arrow-2faced": "./images/arrow-2faced.png",
            "triangle": "./images/triangle.png"
        }

        self.shape_images = []  # Store shape images for reference
        for icon_file_key in self.shape_icons_dict.keys():
            icon_file = self.shape_icons_dict[icon_file_key]
            shape_image = Image.open(icon_file)
            shape_image = shape_image.resize((32, 32), Image.ANTIALIAS)
            shape_icon = ImageTk.PhotoImage(shape_image)
            self.shape_images.append(shape_icon)  # Store shape icons for reference
            shape_button = ttk.Button(shapes_frame, image=shape_icon, command=lambda icon_file_key_=icon_file_key: Draw.set_shape_tool(self, icon_file_key_))
            shape_button.image = shape_icon
            shape_button.pack(side=tk.LEFT, padx=5, pady=5)

        # prev_slide_button = ttk.Button(toolbar, text="⬅️", command=self.prev_slide)
        # prev_slide_button.pack(side=tk.LEFT, padx=5)
            
        # next_slide_button = ttk.Button(toolbar, text="➡️", command=self.next_slide)
        # next_slide_button.pack(side=tk.LEFT, padx=5)

        # add_slide_button = ttk.Button(toolbar, text="➕", command=self.add_slide)
        # add_slide_button.pack(side=tk.LEFT, padx=5)

        prev_slide_image = Image.open("./images/left-arrow.png")  # Replace with your image path
        prev_slide_image = prev_slide_image.resize((32, 32), Image.ANTIALIAS)
        prev_slide_icon = ImageTk.PhotoImage(prev_slide_image)

        next_slide_image = Image.open("./images/right-arrow.png")  # Replace with your image path
        next_slide_image = next_slide_image.resize((32, 32), Image.ANTIALIAS) # Replace
        next_slide_icon = ImageTk.PhotoImage(next_slide_image)

        add_slide_image = Image.open("./images/plus.png")  # Replace with your image path
        add_slide_image = add_slide_image.resize((32, 32), Image.ANTIALIAS) # Replace
        add_slide_icon = ImageTk.PhotoImage(add_slide_image)
        
        download_image = Image.open("./images/download.png") # Replace with your image
        download_image = download_image.resize((32, 32), Image.ANTIALIAS)
        download_icon = ImageTk.PhotoImage(download_image)
        
        delete_image = Image.open("./images/delete.png") # Replace with your
        delete_image = delete_image.resize((32, 32), Image.ANTIALIAS)
        delete_icon = ImageTk.PhotoImage(delete_image)

        # Create navigation buttons with images
        prev_slide_button = ttk.Button(toolbar, image=prev_slide_icon, command=lambda: Setup.prev_slide(self))
        prev_slide_button.image = prev_slide_icon
        prev_slide_button.pack(side=tk.LEFT, padx=5)

        next_slide_button = ttk.Button(toolbar, image=next_slide_icon, command=lambda: Setup.next_slide(self))
        next_slide_button.image = next_slide_icon
        next_slide_button.pack(side=tk.LEFT, padx=5)

        add_slide_button = ttk.Button(toolbar, image=add_slide_icon, command=lambda: Setup.add_slide(self))
        add_slide_button.image = add_slide_icon
        add_slide_button.pack(side=tk.LEFT, padx=5)
        
        save_as_pdf_button = ttk.Button(toolbar, image=download_icon, command=lambda: Setup.save_all_slides_as_pdf(self))
        save_as_pdf_button.image = download_icon
        save_as_pdf_button.pack(side=tk.LEFT, padx=5)
        
        delete_slide_button = ttk.Button(toolbar, image=delete_icon, command=lambda: Setup.delete_current_slide(self))
        delete_slide_button.image = delete_icon
        delete_slide_button.pack(side=tk.LEFT, padx=5)

        # check_button = tk.Button(toolbar, text="Click me!", command=lambda: LoadShapes.get_shapes(self))
        # check_button.pack(side=tk.LEFT, padx=5)



        self.current_color_box = ttk.Label(
            toolbar,
            width=2,
            background=self.background,
            relief=tk.RIDGE,  # Add a relief style for the rounded border
            borderwidth=3,   # Increase borderwidth for a more pronounced effect
            cursor="hand2"   # Change cursor to indicate interactivity
        )
        self.current_color_box.pack(side=tk.LEFT, padx=5)

        # Bind right-click event to the colored box
        self.current_color_box.bind("<Button-3>", lambda event: Setup.change_background_color(self, event))
        



        # Creating meno to handing file options

        # Load the exit button icon
        exit_icon = Image.open("./images/exit.png")  # Replace "exit_icon.png" with your image file path
        exit_icon = exit_icon.resize((1, 1), Image.ANTIALIAS)  # Resize the icon as needed
        exit_icon = ImageTk.PhotoImage(exit_icon)

        # Create a menu bar
        menubar = tk.Menu(self.root)

        # Add the "Exit" button directly to the menu bar
        menubar.add_command(label='Exist', command=lambda : destroy_canvas(self=self))


        # Create the "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save",  command=lambda: SaveCanvas.save(self))
        file_menu.add_command(label="Open", command=lambda: SaveCanvas.open_file(self))

        # Add the "File" menu to the menu bar
        menubar.add_cascade(label="File", menu=file_menu)

        
        # Configure the root window with the menu bar
        self.root.config(menu=menubar)

        label_style = Style()
        label_style.configure("Heading.TLabel", font=("Comic Sans MS", 22, "bold"), padding=22, foreground="blue")
        digital_board_label = ttk.Label(toolbar, text="Digital Board", style="Heading.TLabel")
        digital_board_label.pack(side=tk.RIGHT, padx=10)




    def bind_events(definer=None, self=None):
        self.canvas.bind("<Button-1>", lambda event: Draw.start_drawing(self, event))
        self.canvas.bind("<B1-Motion>", lambda event: Draw.draw(self, event))
        self.canvas.bind("<ButtonRelease-1>", lambda event: Draw.stop_drawing(self, event))

        self.canvas.bind("<MouseWheel>", lambda event: Setup.zoom_with_mouse(self, event))  # Capture mouse scroll events
    
        self.canvas.bind("<Button-3>", lambda event: Setup.show_context_menu(self, event))

        self.root.bind("<Control-z>", lambda event: UndoRedo.undo(self, event))
        self.root.bind("<Control-y>", lambda event: UndoRedo.redo(self, event))




        # Create a right-click context menu
        self.context_menu = Menu(self.canvas, tearoff=0)
        self.context_menu.add_command(label="Paste Image", command=lambda: Setup.paste_image(self))
        self.context_menu.add_command(label="Add Text", command=lambda: Setup.create_text_box(self))

        
if __name__ == "__main__":
    pass