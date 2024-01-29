from imports import *
from .create_drawing import Draw
from .undo_redo import UndoRedo
from .save_canvas import SaveCanvas
from .common_utils import *

class Setup:
    
    def next_slide(self):
        if self.current_slide_index < len(self.slides) - 1:
            self.current_slide_index += 1
            self.canvas.pack_forget()  # Hide the current canvas
            self.canvas = self.slides[self.current_slide_index]
            self.canvas.pack(fill=tk.BOTH, expand=True)  # Show the new canvas
            bind_events()

    def prev_slide(self):
        if self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.canvas.pack_forget()  # Hide the current canvas
            self.canvas = self.slides[self.current_slide_index]
            self.canvas.pack(fill=tk.BOTH, expand=True)  # Show the new canvas
            bind_events()


    def add_slide(self):
        def create_canvas(definer=None, self=None):
            canvas = tk.Canvas(self.root, bg=self.background, width=self.canvas_width, height=self.canvas_height)  # Set the initial dimensions
            canvas.pack(fill=tk.BOTH, expand=True)
            self.slides.append(canvas)


        def bind_events(definer=None, self=None):
            self.canvas.bind("<Button-1>", lambda event: Draw.start_drawing(self, event))
            self.canvas.bind("<B1-Motion>", lambda event: Draw.draw(self, event))
            self.canvas.bind("<ButtonRelease-1>", lambda event: Draw.stop_drawing(self, event))

            self.canvas.bind("<MouseWheel>", lambda event: Setup.zoom_with_mouse(self, event))  # Capture mouse scroll events
        
            self.canvas.bind("<Button-3>", lambda event: Setup.show_context_menu(self, event))

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
            self.context_menu.add_command(label="Paste Image", command=Setup.paste_image)
            self.context_menu.add_command(label="Add Text", command=Setup.create_text_box)
        create_canvas(self=self)
        self.current_slide_index = len(self.slides) - 1
        self.canvas.pack_forget() # Hide the current canvas
        self.canvas = self.slides[self.current_slide_index]
        self.canvas.pack(fill=tk.BOTH, expand=True) # Show the new canvas
        # self.canvas.tkraise()
        bind_events(self=self)  # Re-bind event handlers for the new canvas

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

            print("Background color changed to ", self.erased_areas)

            # Update erased areas with the new background color
            for x1, y1, x2, y2 in self.erased_areas:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')  # Redraw erased area with new background color


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


if __name__ == "__main__":
    pass