from imports import *

class SaveCanvas:
    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "canvas_width": self.canvas.winfo_width(),
                "canvas_height": self.canvas.winfo_height(),
                "pen_strokes": self.get_shapes()
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Save", "Digital board saved successfully.")

    def get_shapes(self):
        shapes = {}
        unique_types = set()
        for item in self.canvas.find_all():
            item_type = self.canvas.type(item)
            unique_types.add(item_type)
            if item_type in ["line", "rectangle", "oval", "polygon"]:
                coords = self.canvas.coords(item)
                shapes[item_type] = shapes.get(item_type, []) + [coords]
            elif item_type == "image":
                image_path = self.canvas.itemcget(item, "image")
                shapes["image"] = shapes.get("image", []) + [image_path]
        
        print("Unique Types : ", unique_types)
        return shapes

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)

            # Clear the canvas before loading
            self.canvas.delete("all")

            # Load pen strokes
            for coords in data['pen_strokes'].get("line", []):
                self.canvas.create_line(coords, fill='black')

            for coords in data['pen_strokes'].get("rectangle", []):
                x1, y1, x2, y2 = coords
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='green')
            
            for coords in data['pen_strokes'].get("oval", []):
                x1, y1, x2, y2 = coords
                self.canvas.create_oval(x1, y1, x2, y2, outline='black', fill='blue')

            for coords in data['pen_strokes'].get("polygon", []):
                points = coords
                self.canvas.create_polygon(points, outline='black', fill='yellow')



if __name__ == "__main__":
    pass