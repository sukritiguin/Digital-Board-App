from imports import *
from tkinter import Canvas
from typing import Dict, ForwardRef
from .fetch_shape_props import *
from . import create_shape_from_props
DigitalBoardType = ForwardRef('DigitalBoard')

def append_to_file(filename='output.txt', text=''):
    with open(filename, 'a') as file:
        file.write(text + '\n')

class LoadShapes:
    def get_shapes(self)->Dict:
        self_canvas: Canvas = self.canvas
        print("Type of self : ", type(self))
        # shapes = {}
        # unique_types = set()
        # for item in self.canvas.find_all():
        #     item_type = self.canvas.type(item)
        #     unique_types.add(item_type)
        #     if item_type in ["line", "rectangle", "oval", "polygon"]:
        #         coords = self.canvas.coords(item)
        #         shapes[item_type] = shapes.get(item_type, []) + [coords]
        #     elif item_type == "image":
        #         image_path = self.canvas.itemcget(item, "image")
        #         shapes["image"] = shapes.get("image", []) + [image_path]
        
        # print("Unique Types : ", unique_types)
        # return shapes
        shapes = {}
        shapes['line'] = []
        shapes['oval'] = []
        shapes['rectangle'] = []
        shapes['polygon'] = []
        for shape in self_canvas.find_all():
            append_to_file(text=str(shape))
            shape_type = self_canvas.type(shape)
            append_to_file(text=str(shape_type))
            if shape_type == "line":
                line_props = get_line_props(self_canvas, shape)
                shapes['line'].append(line_props)
                append_to_file(text=str(line_props))
            if shape_type == "oval":
                oval_props = get_oval_props(self_canvas, shape)
                shapes['oval'].append(oval_props)
                append_to_file(text=str(oval_props))
            if shape_type == "rectangle":
                rectangle_props = get_rectangle_props(self_canvas, shape)
                shapes['rectangle'].append(rectangle_props)
                append_to_file(text=str(rectangle_props))
            if shape_type == "polygon":
                polygon_props = get_polygon_props(self_canvas, shape)
                shapes['polygon'].append(polygon_props)
                append_to_file(text=str(polygon_props))

        return shapes


class SaveCanvas:
    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "canvas_width": self.canvas.winfo_width(),
                "canvas_height": self.canvas.winfo_height(),
                "background_color": self.canvas.cget("background"),
                "pen_strokes": LoadShapes.get_shapes(self)
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Save", "Digital board saved successfully.")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)

            # Clear the canvas before loading
            self.canvas.delete("all")

            self.canvas.config(width=data['canvas_width'], height=data['canvas_height'], bg=data['background_color'])

            for line_props in data['pen_strokes']['line']:
                create_shape_from_props.create_line_from_props(canvas=self.canvas, props=line_props)
            
            for oval_props in data['pen_strokes']['oval']:
                create_shape_from_props.create_oval_from_props(canvas=self.canvas, props=oval_props)

            for rectangle_props in data['pen_strokes']['rectangle']:
                create_shape_from_props.create_rectangle_from_props(canvas=self.canvas, props=rectangle_props)

            for polygon_props in data['pen_strokes']['polygon']:
                create_shape_from_props.create_polygon_from_props(canvas=self.canvas, props=polygon_props)

            # Load pen strokes
            # for coords in data['pen_strokes'].get("line", []):
            #     self.canvas.create_line(coords, fill='black')

            # for coords in data['pen_strokes'].get("rectangle", []):
            #     x1, y1, x2, y2 = coords
            #     self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='green')
            
            # for coords in data['pen_strokes'].get("oval", []):
            #     x1, y1, x2, y2 = coords
            #     self.canvas.create_oval(x1, y1, x2, y2, outline='black', fill='blue')

            # for coords in data['pen_strokes'].get("polygon", []):
            #     points = coords
            #     self.canvas.create_polygon(points, outline='black', fill='yellow')



if __name__ == "__main__":
    pass