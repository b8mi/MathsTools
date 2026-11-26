
import tkinter as tk
import math
from tkinter import messagebox, simpledialog
from copy import deepcopy

MAKER = "Made by:"
NAME = "Azam Albagami"
DATE = "2024/4/21"
HISTORY_LIMIT = 100

letters = [
    "X and Y text box", "Submit", "Lines colors", "Clear lines",
    "-90° & 90° Rotate", "180° Rotate", "270° & -270° Rotate",
    "Displace on Y", "Mirroring", "Displace on X"
]

numbers = [
    "Type the cords\nfor the x and y\npoints in the\ntext rectangle.",
    "Once you type\nthe cords for\nthe lines, press\nsubmit to draw\nthem.",
    "Customise your\nlines color.",
    "Press the clear\nbutton to delete\nall the lines\nyou have drawn.",
    "Rotate your lines\nCounterClockWise\nwith 90°, rotate\nyour lines -90°\nfor ClockWise.",
    "Rotate your lines\n180°.",
    "Rotate your lines\nCounterClockWise\nwith 270°, and\nrotate your lines\n-270° for ClockWise.",
    "Displace your\nlines Up by one\ny+1, and Displace\nyour lines Down\nby one y-1.",
    'Press "V" to\nreflect on Y axis.\nPress "H" to reflect\non X axis.',
    "Displace your lines\nLeft by one x-1,\nand displace your\nlines Right by one\nx+1."
]

explaining = [
    "Draws a line\nbased on the\ngiven (x,y) cords.",
    "No Explanation",
    "No Explanation",
    "No Explanation",
    "Before -90 (x,y)\nAfter -90 (y,-x)\n\nBefore 90 (x,y)\nAfter 90 (-y,x)",
    "Before 180 (x,y)\nAfter 180 (-x,-y)",
    "Before -270 (x,y)\nAfter -270 (-y,x)\n\nBefore 270 (x,y)\nAfter 270 (y,-x)",
    "Before y+1 (x,y)\nAfter y+1 (x,y+1)\n\nBefore y-1 (x,y)\nAfter y-1 (x,y-1)",
    "Before Flip X (x,y)\nAfter Flip X (x,-y)\n\nBefore Flip Y (x,y)\nAfter Flip Y (-x,y)",
    "Before x+1 (x,y)\nAfter x+1 (x+1,y)\n\nBefore x-1 (x,y)\nAfter x-1 (x-1,y)"
]

tutorial_boundaries = [
    (20, 28, 380, 106),
    (6, 130, 115, 175),
    (118, 146, 269, 175),
    (273, 130, 393, 175),
    (15, 216, 158, 265),
    (165, 216, 233, 265),
    (240, 216, 383, 265),
    (5, 302, 126, 346),
    (129, 302, 275, 346),
    (277, 302, 399, 346)
]

current_index = 0
mover = 12

lines = []
selected_colors = []
line_colors = ["green", "#b8860b", "purple"]

undo_stack = []
redo_stack = []


def capture_state():
    return deepcopy(lines), selected_colors.copy()


def restore_state(state):
    global lines, selected_colors

    lines, selected_colors = state

    draw_lines()
    update_history_buttons()


def update_history_buttons():
    if "undo_button" in globals():
        undo_button.config(state=tk.NORMAL if undo_stack else tk.DISABLED)
        redo_button.config(state=tk.NORMAL if redo_stack else tk.DISABLED)


def remember_state():
    undo_stack.append(capture_state())

    if len(undo_stack) > HISTORY_LIMIT:
        undo_stack.pop(0)

    redo_stack.clear()
    update_history_buttons()


def undo():
    if undo_stack:
        redo_stack.append(capture_state())
        restore_state(undo_stack.pop())


def redo():
    if redo_stack:
        undo_stack.append(capture_state())
        restore_state(redo_stack.pop())


def get_selected_color():
    for i, button in enumerate(toggle_buttons):
        if button["relief"] == tk.SUNKEN:
            return i

    return -1


def add_segments(segments):
    remember_state()

    lines.extend(segments)
    selected_colors.extend([get_selected_color()] * len(segments))

    draw_lines()


def transform_points(operation):
    global lines

    if not lines:
        return

    transformed = [[operation(x, y) for x, y in segment] for segment in lines]

    for segment in transformed:
        for point in segment:
            if not all(math.isfinite(n) for n in point):
                messagebox.showerror("Invalid transformation", "Coordinates are too large.")
                return

    if transformed == lines:
        return

    remember_state()

    lines = transformed

    draw_lines()


def rotation_function(degree):
    degree %= 360

    if degree == 0:
        return lambda x, y: (x, y)

    if degree == 90:
        return lambda x, y: (-y, x)

    if degree == 180:
        return lambda x, y: (-x, -y)

    if degree == 270:
        return lambda x, y: (y, -x)

    angle = math.radians(degree)

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    return lambda x, y: (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


def custom_rotation():
    degree = simpledialog.askfloat("Custom rotation", "Enter angle in degrees:", parent=root)

    if degree is None:
        return

    if not math.isfinite(degree):
        messagebox.showerror("Invalid angle", "Enter a finite angle.")
        return

    rotate_lines(degree)


def read_coordinates():
    entries = [xrangle_x, xrangle_y, xrangle_x2, xrangle_y2]
    coordinates = []

    for entry in entries:
        value = entry.get().strip()
        coordinates.append(float(value) if value else 0.0)

    if not all(math.isfinite(n) for n in coordinates):
        raise ValueError("Coordinates must be finite numbers.")

    return coordinates


def submit():
    try:
        x1, y1, x2, y2 = read_coordinates()

    except ValueError as exc:
        messagebox.showerror("Invalid coordinates", str(exc))
        return

    add_segments([[(x1, y1), (x2, y2)]])


def rotate_lines(degree):
    transform_points(rotation_function(degree))


def displace_lines(dx, dy):
    transform_points(lambda x, y: (x + dx, y + dy))


def world_to_canvas(point):
    x, y = point

    center_x = square_x + square_size / 2
    center_y = square_y + square_size / 2

    return center_x + x * cell_size, center_y - y * cell_size


def canvas_to_world(point):
    x, y = point

    center_x = square_x + square_size / 2
    center_y = square_y + square_size / 2

    return (x - center_x) / cell_size, (center_y - y) / cell_size


def resolve_line_color(index):
    if index >= len(selected_colors):
        return "black"

    color_index = selected_colors[index]

    return line_colors[color_index] if color_index != -1 else "black"


def draw_lines():
    canvas.delete("line")

    for i, segment in enumerate(lines):
        color = resolve_line_color(i)

        start = world_to_canvas(segment[0])
        end = world_to_canvas(segment[1])

        if not all(math.isfinite(n) for n in (*start, *end)):
            continue

        canvas.create_line(*start, *end, fill=color, width=1.5, tags="line")


def toggle_button(index):
    for i, button in enumerate(toggle_buttons):
        button.config(relief=tk.SUNKEN if i == index else tk.RAISED)


def clear_lines():
    if not lines:
        return

    remember_state()

    lines.clear()
    selected_colors.clear()

    draw_lines()


def mirror_lines_ony():
    transform_points(lambda x, y: (-x, y))


def mirror_lines_onx():
    transform_points(lambda x, y: (x, -y))


def y_plus_one():
    displace_lines(0, 1)


def y_minus_one():
    displace_lines(0, -1)


def x_minus_one():
    displace_lines(-1, 0)


def x_plus_one():
    displace_lines(1, 0)


def polygon_to_segments(points):
    return [[points[i], points[(i + 1) % len(points)]] for i in range(len(points))]


def draw_square():
    points = [(1.0, 1.0), (1.0, 5.0), (5.0, 5.0), (5.0, 1.0)]

    add_segments(polygon_to_segments(points))


def drawing_bounds():
    if not lines:
        return None

    points = [point for segment in lines for point in segment]

    xs, ys = zip(*points)

    return min(xs), min(ys), max(xs), max(ys)


def drawing_center():
    bounds = drawing_bounds()

    if bounds is None:
        return 0.0, 0.0

    left, bottom, right, top = bounds

    return left / 2 + right / 2, bottom / 2 + top / 2


def scale_lines(scale_x, scale_y, pivot=(0.0, 0.0)):
    if not all(math.isfinite(value) for value in (scale_x, scale_y, *pivot)):
        messagebox.showerror("Invalid scale", "Enter finite scale factors and pivot coordinates.")
        return

    px, py = pivot

    transform_points(lambda x, y: (px + (x - px) * scale_x, py + (y - py) * scale_y))


def custom_scaling():
    if not lines:
        messagebox.showinfo("Scaling", "Draw at least one line first.")
        return

    scale_x = simpledialog.askfloat("Horizontal scaling", "Enter X scale factor:", initialvalue=1.0, parent=root)

    if scale_x is None:
        return

    scale_y = simpledialog.askfloat("Vertical scaling", "Enter Y scale factor:", initialvalue=scale_x, parent=root)

    if scale_y is None:
        return

    use_center = messagebox.askyesnocancel("Scaling pivot", "Scale around the drawing center?\nYes: drawing center\nNo: origin", parent=root)

    if use_center is None:
        return

    pivot = drawing_center() if use_center else (0.0, 0.0)

    scale_lines(scale_x, scale_y, pivot)


def custom_displacement():
    if not lines:
        messagebox.showinfo("Displacement", "Draw at least one line first.")
        return

    dx = simpledialog.askfloat("Horizontal displacement", "Enter X displacement:", initialvalue=0.0, parent=root)

    if dx is None:
        return

    dy = simpledialog.askfloat("Vertical displacement", "Enter Y displacement:", initialvalue=0.0, parent=root)

    if dy is None:
        return

    if not all(math.isfinite(value) for value in (dx, dy)):
        messagebox.showerror("Invalid displacement", "Enter finite values.")
        return

    displace_lines(dx, dy)


def segment_length(segment):
    return math.dist(segment[0], segment[1])


def analyze_geometry():
    bounds = drawing_bounds()

    if bounds is None:
        return None

    left, bottom, right, top = bounds

    lengths = [segment_length(segment) for segment in lines]

    center_x, center_y = drawing_center()

    return {
        "Line segments": len(lines),
        "Unique endpoints": len({tuple(point) for segment in lines for point in segment}),
        "Total line length": f"{sum(lengths):.4g}",
        "Average line length": f"{sum(lengths) / len(lengths):.4g}",
        "Shortest line": f"{min(lengths):.4g}",
        "Longest line": f"{max(lengths):.4g}",
        "Minimum X": f"{left:.4g}",
        "Maximum X": f"{right:.4g}",
        "Minimum Y": f"{bottom:.4g}",
        "Maximum Y": f"{top:.4g}",
        "Drawing width": f"{right - left:.4g}",
        "Drawing height": f"{top - bottom:.4g}",
        "Bounding-box center": f"({center_x:.4g}, {center_y:.4g})"
    }


def show_geometry():
    analysis = analyze_geometry()

    if analysis is None:
        messagebox.showinfo("Geometry analysis", "Draw at least one line first.")
        return

    details = "\n".join(f"{label}: {value}" for label, value in analysis.items())

    messagebox.showinfo("Geometry analysis", details, parent=root)


def highlight_tutorial_control():
    canvas.delete("lines0")

    bounds = tutorial_boundaries[current_index]

    canvas.create_rectangle(*bounds, outline="red", width=2, tags="lines0")


def display_elements(canvas_tutorial):
    canvas_tutorial.delete("elements")

    highlight_tutorial_control()

    canvas_tutorial.create_text(200, 30, text="Graphing Tool Properties:", font=("Arial", 17, "bold"), tags="elements")
    canvas_tutorial.create_text(295, 77, text=letters[current_index], font=("Arial", 14), tags="elements")
    canvas_tutorial.create_text(105, 75, text="Description:", font=("Arial", 18), tags="elements")
    canvas_tutorial.create_line(200, 50, 200, 233, fill="dark grey", width=2, tags="elements")

    canvas_tutorial.create_text(105, 165, text=numbers[current_index], font=("Arial", 14), width=175, tags="elements")
    canvas_tutorial.create_text(300, 160, text=explaining[current_index], font=("Arial", 14), width=185, tags="elements")


def next_element():
    global current_index

    if current_index < len(letters) - 1:
        current_index += 1

        display_elements(canvas_tutorial)
        update_tutorial_buttons()


def previous_element():
    global current_index

    if current_index > 0:
        current_index -= 1

        display_elements(canvas_tutorial)
        update_tutorial_buttons()


def update_tutorial_buttons():
    if current_index == 0:
        back_button.place_forget()

    else:
        back_button.place(x=19, y=243)

    if current_index == len(letters) - 1:
        next_button.place_forget()

    else:
        next_button.place(x=283, y=243)


def build_tutorial_borders():
    borders = [
        (10, 10, 390, 10),
        (10, 10, 10, 290),
        (390, 290, 390, 10),
        (390, 290, 10, 290),
        (10, 50, 390, 50),
        (10, 234, 390, 234),
        (210, 95, 380, 95),
        (20, 95, 190, 95)
    ]

    for coordinates in borders:
        canvas_tutorial.create_line(*coordinates, fill="dark gray", width=2)


def build_tutorial_buttons():
    global next_button, back_button, understood_button

    next_button = tk.Button(page, text="Next", font=("Arial", 14), width=8, command=next_element)
    back_button = tk.Button(page, text="Previous", font=("Arial", 14), width=9, command=previous_element)
    understood_button = tk.Button(page, text="Understood", font=("Arial", 14), width=9, command=understood_button_click)

    next_button.place(x=283, y=243)
    back_button.place(x=19, y=243)
    understood_button.place(x=151, y=243)

    update_tutorial_buttons()


def open_tutorial():
    global page, canvas_tutorial, current_index

    if "page" in globals() and page.winfo_exists():
        page.lift()
        return

    current_index = 0

    root.geometry(f"{width}x{height}+50+200")

    page = tk.Toplevel(root)

    page.title("Tutorial")
    page.geometry("400x300+850+250")
    page.protocol("WM_DELETE_WINDOW", understood_button_click)

    canvas_tutorial = tk.Canvas(page, bg="light grey", width=400, height=300)

    canvas_tutorial.pack(fill="both", expand=True)

    build_tutorial_borders()
    display_elements(canvas_tutorial)
    build_tutorial_buttons()


def understood_button_click():
    global current_index

    canvas.delete("lines0")

    page.destroy()

    root.geometry(f"{width}x{height}+{og_x}+{og_y}")

    current_index = 0


def create_window():
    global root, canvas, width, height, og_x, og_y

    root = tk.Tk()

    root.title("Coordinate Transformations")

    width, height = 800, 400

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    og_x = (screen_width - width) // 2
    og_y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{og_x}+{og_y}")
    root.configure(bg="light grey")
    root.resizable(False, False)

    canvas = tk.Canvas(root, bg="light grey", width=width, height=height)

    canvas.pack(fill="both", expand=True)


def build_grid():
    global square_size, square_x, square_y, cell_size

    square_size = min(width // 2, height - 63)

    square_x = width - square_size - 30
    square_y = (height - square_size) // 2

    canvas.create_rectangle(square_x, square_y, square_x + square_size, square_y + square_size, fill="white", outline="")

    grid_size = 16
    cell_size = square_size / grid_size

    for i in range(grid_size + 1):
        y = square_y + i * cell_size

        color = "blue" if i == grid_size // 2 else "gray"

        canvas.create_line(square_x, y, square_x + square_size, y, fill=color)

    for i in range(grid_size + 1):
        x = square_x + i * cell_size

        color = "red" if i == grid_size // 2 else "gray"

        canvas.create_line(x, square_y, x, square_y + square_size, fill=color)


def create_coordinate_entry(parent, name, row, column):
    label = tk.Label(parent, text=name, bg="light grey", font=("Arial", 14, "bold"))

    label.grid(row=row, column=column, padx=5, pady=5)

    entry = tk.Entry(parent, width=12)

    entry.grid(row=row, column=column + 1, padx=5, pady=5)

    return entry


def build_coordinate_inputs():
    global xrangle_x, xrangle_y, xrangle_x2, xrangle_y2

    input_frame = tk.Frame(root, bg="light grey")

    input_frame.place(x=33, y=29)

    xrangle_x = create_coordinate_entry(input_frame, "x1:", 0, 0)
    xrangle_y = create_coordinate_entry(input_frame, "y1:", 0, 2)

    xrangle_x2 = create_coordinate_entry(input_frame, "x2:", 1, 0)
    xrangle_y2 = create_coordinate_entry(input_frame, "y2:", 1, 2)


def create_button(text, command, x, y, button_width=5, font_size=12):
    button = tk.Button(root, text=text, width=button_width, height=1, font=("Arial", font_size, "bold"), command=command)

    button.place(x=x, y=y)

    return button


def create_label(text, x, y, font_size=12):
    label = tk.Label(root, text=text, bg="light grey", font=("Arial", font_size, "bold"))

    label.place(x=x, y=y)

    return label


def build_rotation_buttons():
    angles = [-90, 90, 180, 270, -270]

    positions = [16, 91, 166, 241, 316]

    for angle, x in zip(angles, positions):
        create_button(f"{angle}°", lambda value=angle: rotate_lines(value), x, 205 + mover, 4, 17)


def build_displacement_buttons():
    controls = [
        ("y+1", y_plus_one),
        ("y-1", y_minus_one),
        ('"V"', mirror_lines_ony),
        ('"H"', mirror_lines_onx),
        ("x-1", x_minus_one),
        ("x+1", x_plus_one)
    ]

    positions = [6, 68, 130, 204, 278, 340]

    for (text, command), x in zip(controls, positions):
        create_button(text, command, x, 291 + mover, 4, 15)


def build_color_buttons():
    global toggle_buttons

    toggle_buttons = []

    color_names = ["green", "yellow", "purple"]

    positions = [120, 172, 224]

    for index, (color, x) in enumerate(zip(color_names, positions)):
        button = create_button(color, lambda i=index: toggle_button(i), x, 136.3 + mover, 5, 9)

        toggle_buttons.append(button)

    create_label("*Lines Colors*", 137, 105 + mover)


def build_history_buttons():
    global undo_button, redo_button

    undo_button = tk.Button(root, text="Undo", command=undo, width=6, state=tk.DISABLED)
    redo_button = tk.Button(root, text="Redo", command=redo, width=6, state=tk.DISABLED)

    angle_button = tk.Button(root, text="Custom angle", command=custom_rotation, width=11)

    undo_button.place(x=450, y=355)
    redo_button.place(x=510, y=355)
    angle_button.place(x=570, y=355)

    root.bind("<Control-z>", lambda event: undo())
    root.bind("<Control-y>", lambda event: redo())


def build_dividers():
    available_width = square_x - 10
    line_end_x = available_width - 20
    vertical_line_x = square_x - 30

    dividers = [
        (0, 183 + mover, line_end_x, 183 + mover),
        (vertical_line_x, 0, vertical_line_x, height),
        (0, 373 + mover, 403, 373 + mover),
        (0, 349 + mover, 403, 349 + mover),
        (278, 349 + mover, 278, 373 + mover),
        (0, 269 + mover, vertical_line_x, 269 + mover),
        (0, 14, line_end_x, 14)
    ]

    for coordinates in dividers:
        canvas.create_line(*coordinates, fill="dark gray", width=2)


def build_controls():
    build_dividers()

    create_button("Submit", submit, 8, 120 + mover, 8, 15)
    create_button("Clear Lines", clear_lines, 275, 120 + mover, 9, 15)

    create_label("   Rotations   ", 30, 172 + mover)
    create_label("Transformations & Mirrors", 30, 257 + mover)
    create_label("      Points     ", 30, 2)

    create_label(f"{MAKER} {NAME}", 15, 350 + mover, 10)
    create_label(DATE, 300, 350 + mover, 10)

    build_rotation_buttons()
    build_displacement_buttons()
    build_color_buttons()
    build_history_buttons()

    create_button("Square", draw_square, 680, 355, 7, 17)
    create_button("?", open_tutorial, 765, 7, 2, 17)


def build_advanced_controls():
    menu = tk.Menu(root, tearoff=False)

    menu.add_command(label="Custom scaling", command=custom_scaling)
    menu.add_command(label="Custom displacement", command=custom_displacement)

    menu.add_separator()

    menu.add_command(label="Geometry analysis", command=show_geometry)

    def open_tools():
        try:
            menu.tk_popup(tools_button.winfo_rootx(), tools_button.winfo_rooty() + tools_button.winfo_height())

        finally:
            menu.grab_release()

    tools_button = create_button("Tools", open_tools, 450, 3, 8, 10)


def main():
    create_window()
    build_grid()
    build_coordinate_inputs()
    build_controls()
    build_advanced_controls()

    root.mainloop()


if __name__ == "__main__":
    main()
