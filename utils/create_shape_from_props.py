from tkinter import *

def create_line_from_props(canvas, props):
    # Extract properties from the dictionary
    coords = props.get('Coordinates', [])
    color = props.get('Color', 'black')
    thickness = float(props.get('Thickness', 1.0))
    dash_pattern = props.get('Dash Pattern', '')
    join_style = props.get('Join Style', 'round')
    cap_style = props.get('Cap Style', 'round')
    smoothness = props.get('Smoothness', True)
    state = props.get('State', NORMAL)
    visibility = props.get('Visibility', '')
    arrow_shape = props.get('Arrow Shape', 'none')
    arrow_size = props.get('Arrow Size', '8 10 3')

    # Create the line
    line_id = canvas.create_line(*coords, fill=color, width=thickness, dash=dash_pattern,
                                  joinstyle=join_style, capstyle=cap_style, smooth=smoothness,
                                  state=state)

    # Add arrow if specified
    if arrow_shape != 'none':
        canvas.itemconfig(line_id, arrow=arrow_shape)

    # Set visibility if specified
    if visibility == 'hidden':
        canvas.itemconfig(line_id, state=HIDDEN)

    return line_id


def create_oval_from_props(canvas, props):
    # Extract properties from the dictionary
    coords = props.get('coords', [])
    outline_color = props.get('outline_color', 'black')
    outline_width = float(props.get('outline_width', 1.0))
    fill_color = props.get('fill_color', '')
    dash_pattern = props.get('dash_pattern', '')
    active_outline_color = props.get('active_outline_color', '')
    active_fill_color = props.get('active_fill_color', '')
    tags = props.get('tags', ())

    # Create the oval
    oval_id = canvas.create_oval(*coords, outline=outline_color, width=outline_width,
                                  fill=fill_color, dash=dash_pattern,
                                  activeoutline=active_outline_color, activefill=active_fill_color,
                                  tags=tags)

    return oval_id

def create_rectangle_from_props(canvas, props):
    # Extract properties from the dictionary
    coords = props.get('coords', [])
    outline_color = props.get('outline_color', 'black')
    outline_width = float(props.get('outline_width', 1.0))
    fill_color = props.get('fill_color', '')
    dash_pattern = props.get('dash_pattern', '')
    active_outline_color = props.get('active_outline_color', '')
    active_fill_color = props.get('active_fill_color', '')
    tags = props.get('tags', ())

    # Create the rectangle
    rectangle_id = canvas.create_rectangle(*coords, outline=outline_color, width=outline_width,
                                            fill=fill_color, dash=dash_pattern,
                                            activeoutline=active_outline_color, activefill=active_fill_color,
                                            tags=tags)

    return rectangle_id


def create_polygon_from_props(canvas, props):
    # Extract properties from the dictionary
    coords = props.get('coords', [])
    outline_color = props.get('outline_color', 'black')
    outline_width = float(props.get('outline_width', 1.0))
    fill_color = props.get('fill_color', '')
    dash_pattern = props.get('dash_pattern', '')
    active_outline_color = props.get('active_outline_color', '')
    active_fill_color = props.get('active_fill_color', '')
    tags = props.get('tags', ())

    # Create the polygon
    polygon_id = canvas.create_polygon(*coords, outline=outline_color, width=outline_width,
                                       fill=fill_color, dash=dash_pattern,
                                       activeoutline=active_outline_color, activefill=active_fill_color,
                                       tags=tags)

    return polygon_id