from imports import *

class UpdateColor:
    def update_recent_colors(self, index):
        for i, recent_color_button in enumerate(self.recent_color_buttons):
            if i == index:
                style = ttk.Style()
                style.configure(recent_color_button["style"], background=self.recent_colors[i])
            else:
                style = ttk.Style()
                style.configure(recent_color_button["style"], background=self.recent_colors[i])

class SetColor:
    def set_recent_color(self, color, index):
        if index >= 0 and index < len(self.recent_colors):
            self.recent_colors[index] = color
        self.pen_color = color
        UpdateColor.update_recent_colors(self, index)

class Draw:
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
                    outline=self.pen_color, width=2, smooth=True
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
                    outline=self.pen_color, width=2, fill=''
                )
        elif self.current_tool == "eraser":
            self.is_drawing = True
            x, y = event.x, event.y
            item = self.canvas.find_closest(x, y)
            if item:
                # Get the coordinates of the item
                x1, y1, x2, y2 = self.canvas.coords(item)
                # Delete iteam to erase
                self.canvas.delete(item)
                # Add the erased area to the list of erased areas
                self.erased_areas.append((x1, y1, x2, y2))

    def draw(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            if self.current_tool == "pen":
                if self.prev_x is not None and self.prev_y is not None:
                    # Draw Bézier curve
                    shape = self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.pen_color, width=self.pen_width, capstyle=tk.ROUND, smooth=tk.TRUE)
                self.prev_x, self.prev_y = x, y
            elif self.current_tool == "eraser":
                shape = self.canvas.create_rectangle(
                    x - self.eraser_width / 2, y - self.eraser_width / 2,
                    x + self.eraser_width / 2, y + self.eraser_width / 2,
                    fill=self.eraser_color, outline=""
                )
            elif self.current_tool == "circle":
                x, y = event.x, event.y
                shape = self.canvas.coords(self.circle,
                    self.prev_x, self.prev_y, x, y
                )
            elif self.current_tool == "square":
                shape = self.canvas.coords(self.square,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "line":
                arrow_points = [
                    self.start_x, self.start_y,
                    x, y,
                    self.start_x + (x - self.start_x) / 2, self.start_y + (y - self.start_y) / 2
                ]
                shape = self.canvas.coords(self.line, *arrow_points)
            elif self.current_tool == "arrow":
                shape = self.canvas.coords(self.arrow,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "arrow-2faced":
                shape = self.canvas.coords(self.arrow_2faced,
                    self.start_x, self.start_y, x, y
                )
            elif self.current_tool == "triangle":
                triangle_points = [
                    self.start_x, self.start_y,
                    x, y,
                    x - (x - self.start_x), y,  # Third point of triangle
                ]
                shape = self.canvas.coords(self.triangle, *triangle_points)
            elif self.current_tool in self.shape_icons_dict.keys():  # Check if the current tool is a shape icon
                shape = self.draw_shape(self.current_tool, x, y)

    def stop_drawing(self, event):
        self.is_drawing = False

    def set_pen_size(self, value):
        self.pen_width = int(float(value))

    def set_eraser_size(self, value):
        self.eraser_width = int(float(value))

    def change_pen_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            SetColor.set_recent_color(self, color, -1)  # Update recent color and selected color

    def change_color_right_click(self, index):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            SetColor.set_recent_color(self, new_color, index)  # Update the specific color button



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
    

if __name__ == "__main__":
    pass