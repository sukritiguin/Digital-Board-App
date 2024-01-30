

def get_line_props(canvas, line_id):
    # Coordinates
    coordinates = canvas.coords(line_id)
    
    # Color
    color = canvas.itemcget(line_id, "fill")
    
    # Thickness
    thickness = canvas.itemcget(line_id, "width")
    
    # Dash Pattern
    dash_pattern = canvas.itemcget(line_id, "dash")
    
    # Tags
    tags = canvas.gettags(line_id)
    
    # Join Style
    join_style = canvas.itemcget(line_id, "join")
    
    # Cap Style
    cap_style = canvas.itemcget(line_id, "cap")
    
    # Smoothness
    smoothness = canvas.itemcget(line_id, "smooth")
    
    # State
    state = canvas.itemcget(line_id, "state")
    
    # Visibility
    visibility = canvas.itemcget(line_id, "state")

    # Arrow Properties
    arrow_shape = canvas.itemcget(line_id, "arrow")
    arrow_size = canvas.itemcget(line_id, "arrowshape")
    # arrow_fill = canvas.itemcget(line_id, "arrowfill")

    return {
        "Coordinates": coordinates,
        "Color": color,
        "Thickness": thickness,
        "Dash Pattern": dash_pattern,
        "Tags": tags,
        "Join Style": join_style,
        "Cap Style": cap_style,
        "Smoothness": smoothness,
        "State": state,
        "Visibility": visibility,
        "Arrow Shape": arrow_shape,
        "Arrow Size": arrow_size,
        # "Arrow Fill": arrow_fill
    }

def get_oval_props(canvas, oval_id):
    properties = {}
    # Coordinates
    properties['coords'] = canvas.coords(oval_id)
    # Outline Color
    properties['outline_color'] = canvas.itemcget(oval_id, 'outline')
    # Outline Width
    properties['outline_width'] = canvas.itemcget(oval_id, 'width')
    # Fill Color
    properties['fill_color'] = canvas.itemcget(oval_id, 'fill')
    # Dash Pattern
    properties['dash_pattern'] = canvas.itemcget(oval_id, 'dash')
    # Active Outline Color
    properties['active_outline_color'] = canvas.itemcget(oval_id, 'activeoutline')
    # Active Fill Color
    properties['active_fill_color'] = canvas.itemcget(oval_id, 'activefill')
    # Tags
    properties['tags'] = canvas.gettags(oval_id)
    return properties

def get_rectangle_props(canvas, rectangle_id):
    properties = {}
    # Coordinates
    properties['coords'] = canvas.coords(rectangle_id)
    # Outline Color
    properties['outline_color'] = canvas.itemcget(rectangle_id, 'outline')
    # Outline Width
    properties['outline_width'] = canvas.itemcget(rectangle_id, 'width')
    # Fill Color
    properties['fill_color'] = canvas.itemcget(rectangle_id, 'fill')
    # Dash Pattern
    properties['dash_pattern'] = canvas.itemcget(rectangle_id, 'dash')
    # Active Outline Color
    properties['active_outline_color'] = canvas.itemcget(rectangle_id, 'activeoutline')
    # Active Fill Color
    properties['active_fill_color'] = canvas.itemcget(rectangle_id, 'activefill')
    # Tags
    properties['tags'] = canvas.gettags(rectangle_id)
    return properties

def get_polygon_props(canvas, polygon_id):
    properties = {}
    # Coordinates
    properties['coords'] = canvas.coords(polygon_id)
    # Outline Color
    properties['outline_color'] = canvas.itemcget(polygon_id, 'outline')
    # Outline Width
    properties['outline_width'] = canvas.itemcget(polygon_id, 'width')
    # Fill Color
    properties['fill_color'] = canvas.itemcget(polygon_id, 'fill')
    # Dash Pattern
    properties['dash_pattern'] = canvas.itemcget(polygon_id, 'dash')
    # Active Outline Color
    properties['active_outline_color'] = canvas.itemcget(polygon_id, 'activeoutline')
    # Active Fill Color
    properties['active_fill_color'] = canvas.itemcget(polygon_id, 'activefill')
    # Tags
    properties['tags'] = canvas.gettags(polygon_id)
    return properties
