import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, messagebox, Menu
from PIL import Image, ImageTk, ImageGrab
import math
from tkinter.simpledialog import askstring
import tkinter.filedialog as filedialog
from ttkbootstrap import Style


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
import img2pdf
import io
import pyperclip

import base64

import pickle

class DigitalBoard:
    def __init__(self, root):
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
    

        self.create_canvas()
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
        self.create_toolbar()
        


        
        # Create a right-click context menu
        self.context_menu = Menu(self.canvas, tearoff=0)
        self.context_menu.add_command(label="Paste Image", command=self.paste_image)
        self.context_menu.add_command(label="Add Text", command=self.create_text_box)
                
        self.bind_events()
        

    def create_canvas(self):
        canvas = tk.Canvas(self.root, bg=self.background, width=self.canvas_width, height=self.canvas_height)  # Set the initial dimensions
        canvas.pack(fill=tk.BOTH, expand=True)
        self.slides.append(canvas)



    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        
        pen_image = Image.open("./images/pen.png")  # Replace with the path to your pen icon image
        pen_image = pen_image.resize((32, 32), Image.ANTIALIAS)
        pen_icon = ImageTk.PhotoImage(pen_image)
        pen_button = ttk.Button(toolbar, image=pen_icon, command=lambda: self.set_tool("pen"))
        pen_button.image = pen_icon
        pen_button.pack(side=tk.LEFT, padx=5)
        
        pen_size_slider = ttk.Scale(toolbar, from_=2, to=20, orient="horizontal", length=100, command=self.set_pen_size)
        pen_size_slider.set(self.pen_width)
        pen_size_slider.pack(side=tk.LEFT, padx=5)
        
        eraser_image = Image.open("./images/eraser.jpg")  # Replace with the path to your eraser icon image
        eraser_image = eraser_image.resize((32, 32), Image.ANTIALIAS)
        eraser_icon = ImageTk.PhotoImage(eraser_image)
        eraser_button = ttk.Button(toolbar, image=eraser_icon, command=lambda: self.set_tool("eraser"))
        eraser_button.image = eraser_icon
        eraser_button.pack(side=tk.LEFT, padx=5)
        
        eraser_size_slider = ttk.Scale(toolbar, from_=20, to=100, orient="horizontal", length=100, command=self.set_eraser_size)
        eraser_size_slider.set(self.eraser_width)
        eraser_size_slider.pack(side=tk.LEFT, padx=5)
        
        self.recent_color_buttons = []
        for i, recent_color in enumerate(self.recent_colors):
            style = Style()
            style.configure(recent_color + ".TButton", background=recent_color, foreground=recent_color)
            recent_color_button = ttk.Button(toolbar, text="", width=2, style=recent_color + ".TButton",
                                            command=lambda color=recent_color, index=i: self.set_recent_color(color, index))
            recent_color_button.pack(side=tk.LEFT, padx=2)
            self.recent_color_buttons.append(recent_color_button)
            
            # Bind right mouse click to change color of the specific button
            recent_color_button.bind("<Button-3>", lambda event, color=recent_color, index=i: self.change_color_right_click(event, color, index))

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
            shape_button = ttk.Button(shapes_frame, image=shape_icon, command=lambda icon_file_key_=icon_file_key: self.set_shape_tool(icon_file_key_))
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
        prev_slide_button = ttk.Button(toolbar, image=prev_slide_icon, command=self.prev_slide)
        prev_slide_button.image = prev_slide_icon
        prev_slide_button.pack(side=tk.LEFT, padx=5)

        next_slide_button = ttk.Button(toolbar, image=next_slide_icon, command=self.next_slide)
        next_slide_button.image = next_slide_icon
        next_slide_button.pack(side=tk.LEFT, padx=5)

        add_slide_button = ttk.Button(toolbar, image=add_slide_icon, command=self.add_slide)
        add_slide_button.image = add_slide_icon
        add_slide_button.pack(side=tk.LEFT, padx=5)
        
        save_as_pdf_button = ttk.Button(toolbar, image=download_icon, command=self.save_all_slides_as_pdf)
        save_as_pdf_button.image = download_icon
        save_as_pdf_button.pack(side=tk.LEFT, padx=5)
        
        delete_slide_button = ttk.Button(toolbar, image=delete_icon, command=self.delete_current_slide)
        delete_slide_button.image = delete_icon
        delete_slide_button.pack(side=tk.LEFT, padx=5)     


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
        self.current_color_box.bind("<Button-3>", self.change_background_color)
        
        label_style = Style()
        label_style.configure("Heading.TLabel", font=("Comic Sans MS", 22, "bold"), padding=22, foreground="blue")
        digital_board_label = ttk.Label(toolbar, text="Digital Board", style="Heading.TLabel")
        digital_board_label.pack(side=tk.RIGHT, padx=10)




    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.canvas.bind("<MouseWheel>", self.zoom_with_mouse)  # Capture mouse scroll events
    
        self.canvas.bind("<Button-3>", self.show_context_menu)

        


        
        # self.canvas.bind("<Button-3>", self.create_text_box)


    def set_tool(self, tool):
        self.current_tool = tool

    def set_shape_tool(self, tool):
        self.current_tool = tool

    def start_drawing(self, event):
        if self.current_tool in ["pen" , "circle", "square", "line", "arrow", "arrow-2faced", "triangle"]:
            self.is_drawing = True
            x, y = event.x, event.y
            self.prev_x, self.prev_y = x, y
            self.start_x, self.start_y = x, y
            
            print("==="*25)
            print(f"Before {self.current_tool} : ",self.prev_x, ", ",self.prev_y)
            print("==="*25)
            
            if self.current_tool == "circle":
                print("==="*25)
                print("Circle : ",self.prev_x, ", ",self.prev_y)
                print("==="*25)
                self.circle = self.canvas.create_oval(
                    self.prev_x, self.prev_x, self.prev_x, self.prev_y,
                    outline=self.pen_color, width=2
                )
            
            if self.current_tool == "square":
                self.square = self.canvas.create_rectangle(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline=self.pen_color, width=2
                )
                
            if self.current_tool == "line":
                self.line = self.canvas.create_polygon(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline=self.pen_color, width=2
                )
                
            if self.current_tool == "arrow":
                # Draw an arrow using create_line with an arrow at the last point
                self.arrow = self.canvas.create_line(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    fill=self.pen_color, width=2, arrow=tk.LAST
                )
            
            if self.current_tool == "arrow-2faced":
                self.arrow_2faced = self.canvas.create_line(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    fill=self.pen_color, width=2, arrow=tk.BOTH
                )
            
            if self.current_tool == "triangle":
                self.triangle = self.canvas.create_polygon(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline=self.pen_color, width=2, fill=self.background
                )
        elif self.current_tool == "eraser":
            self.is_drawing = True
            x, y = event.x, event.y
            item = self.canvas.find_closest(x, y)
            if item:
                self.canvas.delete(item)

    def draw(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            if self.current_tool == "pen":
                if self.prev_x is not None and self.prev_y is not None:
                    # Draw Bézier curve
                    self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.pen_color, width=self.pen_width, capstyle=tk.ROUND, smooth=tk.TRUE)
                self.prev_x, self.prev_y = x, y
            elif self.current_tool == "eraser":
                self.canvas.create_rectangle(
                    x - self.eraser_width / 2, y - self.eraser_width / 2,
                    x + self.eraser_width / 2, y + self.eraser_width / 2,
                    fill=self.eraser_color, outline=""
                )
            elif self.current_tool == "circle":
                x, y = event.x, event.y
                self.canvas.coords(self.circle,
                    self.prev_x, self.prev_y, x, y
                )
            elif self.current_tool == "square":
                self.canvas.coords(self.square,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "line":
                arrow_points = [
                    self.start_x, self.start_y,
                    x, y,
                    self.start_x + (x - self.start_x) / 2, self.start_y + (y - self.start_y) / 2
                ]
                self.canvas.coords(self.line, *arrow_points)
            elif self.current_tool == "arrow":
                self.canvas.coords(self.arrow,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "arrow-2faced":
                self.canvas.coords(self.arrow_2faced,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "triangle":
                triangle_points = [
                    self.start_x, self.start_y,
                    x, y,
                    x - (x - self.start_x), y,  # Third point of triangle
                ]
                self.canvas.coords(self.triangle, *triangle_points)
            elif self.current_tool in self.shape_icons_dict.keys():  # Check if the current tool is a shape icon
                self.draw_shape(self.current_tool, x, y)

    def stop_drawing(self, event):
        self.is_drawing = False

    def set_pen_size(self, value):
        self.pen_width = int(float(value))

    def set_eraser_size(self, value):
        self.eraser_width = int(float(value))

    def change_pen_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.set_recent_color(color, -1)  # Update recent color and selected color

    def change_color_right_click(self, event, color, index):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            self.set_recent_color(new_color, index)  # Update the specific color button

    def set_recent_color(self, color, index):
        if index >= 0 and index < len(self.recent_colors):
            self.recent_colors[index] = color
        self.pen_color = color
        self.update_recent_colors(index)

    def update_recent_colors(self, index):
        for i, recent_color_button in enumerate(self.recent_color_buttons):
            if i == index:
                style = ttk.Style()
                style.configure(recent_color_button["style"], background=self.recent_colors[i])
            else:
                style = ttk.Style()
                style.configure(recent_color_button["style"], background=self.recent_colors[i])

    def draw_shape(self, shape_type, x, y):
        # shape_type = None

        # # Determine the shape type based on the selected tool (image)
        # if shape_image == self.shape_images[0]:
        #     shape_type = "rectangle"
        # elif shape_image == self.shape_images[1]:
        #     shape_type = "circle"
        # elif shape_image == self.shape_images[2]:
        #     shape_type = "square"
        # elif shape_image == self.shape_images[3]:
        #     shape_type = "line"
        # elif shape_image == self.shape_images[4]:
        #     shape_type = "arrow"
        # elif shape_image == self.shape_images[5]:
        #     shape_type = "two-faced arrow"
        # elif shape_image == self.shape_images[6]:
        #     shape_type = "triangle"

        if shape_type:
            self.draw_shape_by_type(shape_type, x, y)

    def draw_shape_by_type(self, shape_type, x, y):
        if shape_type == "rectangle":
            self.draw_rectangle(x, y)
        elif shape_type == "circle":
            self.draw_circle(x, y)
        elif shape_type == "square":
            self.draw_square(x, y)
        elif shape_type == "line":
            self.draw_line(x, y)
        elif shape_type == "arrow":
            self.draw_arrow(x, y)
        elif shape_type == "arrow-2faced":
            self.draw_two_faced_arrow(x, y)
        elif shape_type == "triangle":
            self.draw_triangle(x, y)

    def draw_rectangle(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            self.shapes.append(self.canvas.create_rectangle(self.prev_x, self.prev_y, x, y, outline=self.pen_color, width=self.pen_width))

    def draw_circle(self, x, y):
        # if self.prev_x is not None and self.prev_y is not None:
        #     radius = ((x - self.prev_x) ** 2 + (y - self.prev_y) ** 2) ** 0.5
        #     self.shapes.append(self.canvas.create_oval(self.prev_x - radius, self.prev_y - radius, self.prev_x + radius, self.prev_y + radius, outline=self.pen_color, width=self.pen_width))
        if self.drawing:
            self.canvas.coords(self.circle,
                self.prev_x, self.prev_y, x, y
            )
    def draw_square(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            side_length = min(abs(x - self.prev_x), abs(y - self.prev_y))
            if x < self.prev_x:
                x = self.prev_x - side_length
            else:
                x = self.prev_x
            if y < self.prev_y:
                y = self.prev_y - side_length
            else:
                y = self.prev_y
            self.shapes.append(self.canvas.create_rectangle(x, y, x + side_length, y + side_length, outline=self.pen_color, width=self.pen_width))

    def draw_line(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            self.shapes.append(self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.pen_color, width=self.pen_width, capstyle=tk.ROUND, smooth=tk.TRUE))

    def draw_arrow(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            self.shapes.append(self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.pen_color, width=self.pen_width, arrow=tk.LAST))

    def draw_two_faced_arrow(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            # Calculate the angle between two points
            angle = self.calculate_angle(self.prev_x, self.prev_y, x, y)

            # Draw an arrow with two arrowheads
            self.shapes.append(self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.pen_color, width=self.pen_width, arrow=tk.BOTH, arrowshape=(10, 20, 5)))

    def draw_triangle(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            # Calculate triangle vertices based on mouse position
            vertices = [
                self.prev_x, self.prev_y,
                x, y,
                self.prev_x + (x - self.prev_x) * 2, y
            ]
            self.shapes.append(self.canvas.create_polygon(vertices, outline=self.pen_color, width=self.pen_width))

    def calculate_angle(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return math.degrees(math.atan2(dy, dx))
    
    
    def next_slide(self):
        if self.current_slide_index < len(self.slides) - 1:
            self.current_slide_index += 1
            self.canvas.pack_forget()  # Hide the current canvas
            self.canvas = self.slides[self.current_slide_index]
            self.canvas.pack(fill=tk.BOTH, expand=True)  # Show the new canvas
            self.bind_events()

    def prev_slide(self):
        if self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.canvas.pack_forget()  # Hide the current canvas
            self.canvas = self.slides[self.current_slide_index]
            self.canvas.pack(fill=tk.BOTH, expand=True)  # Show the new canvas
            self.bind_events()


    def add_slide(self):
        self.create_canvas()
        self.current_slide_index = len(self.slides) - 1
        self.canvas.pack_forget() # Hide the current canvas
        self.canvas = self.slides[self.current_slide_index]
        self.canvas.pack(fill=tk.BOTH, expand=True) # Show the new canvas
        # self.canvas.tkraise()
        self.bind_events()  # Re-bind event handlers for the new canvas

    def save_all_slides_as_pdf(self):
        # Prompt the user to choose a directory for saving image files
        save_dir = filedialog.askdirectory(title="Select a Directory to Save Images")
        if not save_dir:
            return

        image_paths = []  # List to store paths of saved image files

        # Save each slide as an image (PNG or JPG) in the selected directory
        for slide_index, slide_canvas in enumerate(self.slides):
            slide_image = slide_canvas.postscript(colormode="color")
            slide_image = Image.open(io.BytesIO(slide_image.encode("utf-8")))
            # slide_image = slide_image.convert("RGB")

            image_file_path = os.path.join(save_dir, f"slide_{slide_index + 1}.png")  # Change extension as needed
            slide_image.save(image_file_path, "png")  # Change format as needed

            image_paths.append(image_file_path)

        # Prompt the user to choose a location and file name for saving the PDF
        pdf_file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            title="Save All Slides as PDF"
        )

        if pdf_file_path:
            # Combine the saved images into a single PDF file using img2pdf
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(img2pdf.convert(image_paths))


    def change_background_color(self, event):
        # Use the colorchooser to let the user pick a new background color
        color = colorchooser.askcolor(initialcolor=self.background)[1]

        if color:
            # Update the background color of the canvas
            self.canvas.configure(bg=color)
            self.background = color  # Update the background color attribute
            self.current_color_box.configure(background=color)  # Update the color box
            self.eraser_color = color # Update the eraser color attribute

    def delete_current_slide(self):
        if len(self.slides) > 1:
            # Remove the canvas widget of the current slide
            self.canvas.destroy()

            # Remove the current slide from the list of slides
            self.slides.pop(self.current_slide_index)

            # Update the current slide index
            if self.current_slide_index >= len(self.slides):
                self.current_slide_index = len(self.slides) - 1

            # Display the new current slide
            self.canvas = self.slides[self.current_slide_index]
            self.canvas.pack(fill=tk.BOTH, expand=True)


    def zoom_with_mouse(self, event):
        delta = event.delta  # Get the scroll direction (positive for zoom in, negative for zoom out)
        zoom_factor = 1.1  # You can adjust the zoom factor as needed

        if delta > 0:
            # Zoom in
            self.canvas_scale *= zoom_factor
            self.canvas_width *= zoom_factor
            self.canvas_height *= zoom_factor
        elif delta < 0:
            # Zoom out
            self.canvas_scale /= zoom_factor
            self.canvas_width /= zoom_factor
            self.canvas_height /= zoom_factor

        # Update the canvas size and scale
        self.update_canvas_size()

    def update_canvas_size(self):
        # Set the new canvas dimensions and scale
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

        # Adjust the scale of the objects on the canvas
        self.canvas.scale("all", 0, 0, self.canvas_scale, self.canvas_scale)

    def paste_image(self):
        # Get image data from clipboard
        clipboard_data = pyperclip.paste()

        # Check if the clipboard data is a valid image
        try:
            # Attempt to get an image from the clipboard
            image = ImageGrab.grabclipboard()

            if image:
                img = ImageTk.PhotoImage(image)
                # x, y = self.canvas.canvasx(self.canvas.winfo_pointerx()), self.canvas.canvasy(self.canvas.winfo_pointery())
                # x, y = self.canvas.canvasx(self.paste_image_x, self.canvas.canvasy(self.paste_image_y))
                self.canvas.create_image(self.paste_image_x, self.paste_image_y, anchor=tk.CENTER, image=img)
                # self.canvas.image = img  # Save a reference to prevent it from being garbage collected
                self.canvas_image.append(img)

                
            else:
                print("Clipboard does not contain a valid image.")
        except Exception as e:
            print(f"Failed to paste image: {e}")


    # Bind the right-click event to the canvas
    def show_context_menu(self, event):
        # self.context_menu.post(event.x_root, event.y_root)
        # self.paste_image_x = event.x_root
        # self.paste_image_y = event.y_root
    # Determine the canvas coordinates of the right-click event
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        # Check if there's an existing object at the clicked position
        item = self.canvas.find_closest(x, y)

        # Post the context menu at the correct position
        if item:
            # If an object is clicked, post the menu at the object's coordinates
            self.context_menu.post(event.x_root, event.y_root)
        else:
            # If the user right-clicked on an empty area, post the menu at that position
            self.context_menu.entryconfigure("Add Text", state=tk.NORMAL)  # Enable "Add Text" option
            self.context_menu.post(event.x_root, event.y_root)

        # Update the coordinates for other actions (e.g., paste image)
        self.paste_image_x, self.paste_image_y = event.x_root, event.y_root
        
        
    def create_text_box(self):
        # x, y = self.canvas.canvasx(self.paste_image_x), self.canvas.canvasy(self.paste_image_y)
        # text = simpledialog.askstring("Add Text", "Enter your text:")
        # if text:
        #     text_box = self.canvas.create_text(x, y, text=text, fill=self.text_color, font=self.font, anchor=tk.NW)
        #     self.text_boxes.append(text_box)  # Maintain a list of text boxes for further manipulation

        x, y = self.canvas.canvasx(self.paste_image_x), self.canvas.canvasy(self.paste_image_y)

        # Prompt the user for text input, color, size, and font
        text = simpledialog.askstring("Add Text", "Enter your text:")
        text_color = colorchooser.askcolor(initialcolor=self.text_color)[1]
        text_size = simpledialog.askinteger("Text Size", "Enter text size:", initialvalue=self.font[1])
        text_font = askstring("Font", "Enter font (e.g., Arial, 12, bold):", initialvalue=f"{self.font[0]}, {self.font[1]}, {self.font[2]}")

        if text:
            text_box = self.canvas.create_text(
                x, y, text=text, fill=text_color, font=(text_font, text_size), anchor=tk.NW
            )
            self.text_boxes.append(text_box)



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
