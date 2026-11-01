import tkinter as tk
import math
from tkinter import messagebox
MAKER = "  Made by:"
NAME  = "B8MI"
DATE  = "   2024/4/21"
SPACER = " "
letters = ["X and Y text box", "Submit", "Lines colors", "Clear lines", "-90° & 90° Rotate", "180° Rotate", "270° & -270° Rotate", "Displace on Y", "Mirroring", "Displace on X"]
numbers = ["Type the cords\nfor the x and y\npoints in the\ntext rectangle.\n", "Once you type\nthe cords for \nthe lines, press\nsubmit to draw\nthem.", "Customise your\nlines color.\n\n\n", "Press the clear\nbutton to delete\nall the lines\nyou have drawn.\n", "Rotate your lines\nCounterClockWise\nwith 90°, rotate\nyour lines -90°\nfor ClockWise.", "Rotate your lines\n180°.\n\n\n", "Rotate your lines\nCounterClockWise\nwith 270°, and \nrotate your lines \n-270°for ClockWise.", "Displace your\nlines Up by one\ny+1,and Displace\nyour lines Down\nby one y-1", "press \"V\" to\nreflect on Y axis,\nvertical mirror.\n\"H\" to reflect on\nX axis, horizontal.", "Displace your lines\nLeft by one x-1,\nand displace your\nlines Right by one\nx+1."]#a
explaining = ["Draws a line \nbased on the \ngiven(x,y) cords.", "No Explaination", "No Explaination", "No Explaination", "before -90 ( x, y)\nafter    -90 ( y,-x)\n\nbefore  90 ( x, y)\nafter     90 (-y, x)", "before 180 ( x, y)\nafter    180 (-x,-y)", "before -270 ( x, y)\nafter    -270 (-y, x)\n\nbefore 270 ( x, y)\nafter    270 ( y,-x)",  "before y+1(x, y)\nafter    y+1(x,y+1)\n\nbefore  y-1(x, y)\nafter     y-1(x,y-1)", "Before Flip x (x, y)\nafter    Flip x (x,-y)\nBefore Flip y ( x,y)\nafter    Flip y (-x,y)", "before x+1( x,y)\nafter    x+1(x+1,y)\n\nbefore  x-1( x,y)\nafter     x-1(x-1,y)"]

explaining_fonts_style =[ 18, 18, 18, 18, 18, 18, 18, 18, 16, 18]
explaining_placementx = [303,295,295,295,295,296,295,296,300,296]
explaining_placementy = [140,120,120,120,162,124,162,162,160,162]
#locate
lines_in_graphing_tool_u = [[20, 28, 380, 28], [6, 130, 115, 130], [118, 146, 269, 146], [393, 130, 273, 130], [15, 216, 158, 216], [165, 216, 233, 216], [240, 216, 383, 216], [5, 302, 126, 302], [129, 302, 275, 302], [277, 302, 399, 302]]
lines_in_graphing_tool_d = [[20, 106, 380, 106], [6, 174, 115, 174], [118, 174, 269, 174], [393, 174, 273, 174], [15, 264, 158, 264], [165, 264, 233, 264], [240, 264, 383, 264], [5, 345, 126, 345], [129, 345, 275, 345], [277, 345, 399, 345]]
lines_in_graphing_tool_l = [[20, 28, 20, 106], [6, 130, 6, 175], [118, 146, 118, 175], [273, 130, 273, 174], [15, 216, 15, 265], [165, 216, 165, 264], [240, 216, 240, 264], [5, 302, 5, 346], [129, 302, 129, 345], [277, 302, 277, 345]]
lines_in_graphing_tool_r = [[380, 28, 380, 106], [114, 130, 114, 175], [269, 146, 269, 175], [393, 130, 393, 175], [157, 216, 157, 265], [232, 216, 232, 264],[382, 216, 382, 264], [126, 302, 126, 346], [274, 302, 274, 345], [398, 302, 398, 345]]
fonts_style =[ 18, 18, 18, 18, 16, 18, 15, 17, 16, 15]
placementx = [105,105,105,111,110,108,111,110,105,106]
placementy = [165,165,165,165,158,165,155,162,160,156]

current_index = 0

mover = 12

next_button_click_count = 0

lines = []

selected_colors = []

line_colors = ["green", "#b8860b", "purple"]

def submit():
    global lines, selected_colors
    
    x_input = xrangle_x.get().strip()
    y_input = xrangle_y.get().strip()
    x_input2 = xrangle_x2.get().strip()
    y_input2 = xrangle_y2.get().strip()

    # Empty coordinate fields represent zero; reject invalid numeric inputs.
    try:
        x_value = float(x_input) if x_input else 0.0
        y_value = float(y_input) if y_input else 0.0
        x2_value = float(x_input2) if x_input2 else 0.0
        y2_value = float(y_input2) if y_input2 else 0.0
    except ValueError:
        messagebox.showerror("Invalid coordinates", "Enter numbers for the four coordinates.")
        return
    if not all(math.isfinite(n) for n in (x_value, y_value, x2_value, y2_value)):
        messagebox.showerror("Invalid coordinates", "Coordinates must be finite numbers.")
        return
    
    color_index = -1
    
    for i, toggle_button in enumerate(toggle_buttons):
        if toggle_button['relief'] == tk.SUNKEN:
            color_index = i
            break

    lines.append([(x_value, y_value), (x2_value, y2_value)])
    selected_colors.append(color_index)
    
    draw_lines()

def rotate_lines(degree):
    global lines
    for i in range(len(lines)):
        x1, y1 = lines[i][0]
        x2, y2 = lines[i][1]
        if degree == 90 or degree == -270:
            lines[i] = [(-y1, x1), (-y2, x2)]
        elif degree == -90 or degree == 270:
            lines[i] = [(y1, -x1), (y2, -x2)]
        elif degree == 180 or degree == -180:
            lines[i] = [(-x1, -y1), (-x2, -y2)]
    draw_lines()

def displace_lines(dx, dy):
    global lines
    for i in range(len(lines)):
        lines[i] = [tuple(coord + delta for coord, delta in zip(point, (dx, dy))) for point in lines[i]]
    draw_lines()

def draw_lines():
    canvas.delete("line")

    for i, line in enumerate(lines):
        color_index = selected_colors[i] if i < len(selected_colors) else -1
        line_color = line_colors[color_index] if color_index != -1 else "black"
        
        start_x = (601 + ((6.2 * line[0][0]) / 100) * square_size)
        start_y = -138 + square_size - ((6.22 * line[0][1]) / 100) * square_size
        end_x = 601 + ((6.2 * line[1][0]) / 100) * square_size
        end_y = -138 + square_size - ((6.22 * line[1][1]) / 100) * square_size
        
        canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=1.5, tags="line")

def toggle_button(index):
    for i in range(len(toggle_buttons)):
        if i == index:
            toggle_buttons[i].config(relief=tk.SUNKEN)
        else:
            toggle_buttons[i].config(relief=tk.RAISED)

def clear_lines():
    global lines, selected_colors
    lines = []
    selected_colors = []
    canvas.delete("line")

def mirror_lines_ony():
    global lines
    for i in range(len(lines)):
        x1, y1 = lines[i][0]
        x2, y2 = lines[i][1]
        lines[i] = [(-x1, y1), (-x2, y2)]
    draw_lines()

def mirror_lines_onx():
    global lines
    for i in range(len(lines)):
        x1, y1 = lines[i][0]
        x2, y2 = lines[i][1]
        lines[i] = [(x1, -y1), (x2, -y2)]
    draw_lines()

def y_plus_one():
    displace_lines(0, 1)

def y_minus_one():
    displace_lines(0, -1)

def x_minus_one():
    displace_lines(-1, 0)

def display_elements(canvas_tutorial):
    global current_index
    global canvas

    global lines_in_graphing_tool_u
    global lines_in_graphing_tool_d
    global lines_in_graphing_tool_l
    global lines_in_graphing_tool_r
    global a, b, c, d
    

    canvas_tutorial.delete("elements")
    canvas.delete("lines0")

    a = (lines_in_graphing_tool_u[current_index][0], lines_in_graphing_tool_u[current_index][1], lines_in_graphing_tool_u[current_index][2], lines_in_graphing_tool_u[current_index][3])
    b = (lines_in_graphing_tool_d[current_index][0], lines_in_graphing_tool_d[current_index][1], lines_in_graphing_tool_d[current_index][2], lines_in_graphing_tool_d[current_index][3])
    c = (lines_in_graphing_tool_l[current_index][0], lines_in_graphing_tool_l[current_index][1], lines_in_graphing_tool_l[current_index][2], lines_in_graphing_tool_l[current_index][3])
    d = (lines_in_graphing_tool_r[current_index][0], lines_in_graphing_tool_r[current_index][1], lines_in_graphing_tool_r[current_index][2], lines_in_graphing_tool_r[current_index][3])
    
    canvas.create_line(a, fill='red', width=2, tags="lines0")
    canvas.create_line(b, fill='red', width=2, tags="lines0")
    canvas.create_line(c, fill='red', width=2, tags="lines0")
    canvas.create_line(d, fill='red', width=2, tags="lines0")

    canvas_tutorial.create_text(295, 77, text=letters[current_index], font=("Arial", 15), fill="black", tags="elements")
    canvas_tutorial.create_text(105, 75, text="Description:", font=("Arial", 20), fill="black", tags="elements")
    canvas_tutorial.create_line(200, 50, 200, 233, fill='dark grey', width=2, tags="elements")

    canvas_tutorial.create_text(placementx[current_index], placementy[current_index], text=numbers[current_index], font=("Arial", fonts_style[current_index]), fill="black", tags="elements")
    canvas_tutorial.create_text(explaining_placementx[current_index], explaining_placementy[current_index], text=explaining[current_index], font=("Arial", explaining_fonts_style[current_index]), fill="black", tags="elements")

    canvas_tutorial.create_text(200, 30, text="Graphing Tool Properties:", font=("Arial", 17, "bold"), fill="black", tags="elements")

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


def x_plus_one():
    displace_lines(1, 0)

def draw_square():
    global lines, selected_colors
    square_lines = [
        [(1.0, 1.0), (1.0, 5.0)],
        [(5.0, 5.0), (1.0, 5.0)],
        [(5.0, 1.0), (5.0, 5.0)],
        [(1.0, 1.0), (5.0, 1.0)]
    ]
    color_index = -1
    for i, toggle_button in enumerate(toggle_buttons):
        if toggle_button['relief'] == tk.SUNKEN:
            color_index = i
            break
    lines.extend(square_lines)
    selected_colors.extend([color_index] * len(square_lines))
    draw_lines()
 
def open_tutorial():
    global page, canvas_tutorial, current_index
    if 'page' in globals() and page.winfo_exists():
        page.lift()
        return
    current_index = 0
    global next_button, back_button
    global understood_button
    global next_button_click_count
    root.geometry(f"{width}x{height}+{50}+{200}")
    page = tk.Toplevel(root)
    page.title("Tutorial")
    page.protocol("WM_DELETE_WINDOW", understood_button_click)
    page.geometry("400x300+850+250")

    canvas_tutorial = tk.Canvas(page, bg='light grey', width=width, height=height)
    canvas_tutorial.pack(fill='both', expand=True)
    display_elements(canvas_tutorial)

    # LINES # LINES # LINES # LINES # LINES # LINES # LINES # LINES # LINES # LINES # LINES #
    canvas_tutorial.create_line(10, 10, 390, 10, fill='dark gray', width=2)
    canvas_tutorial.create_line(10, 10, 10, 290, fill='dark gray', width=2)
    canvas_tutorial.create_line(390, 290, 390, 10, fill='dark gray', width=2)
    canvas_tutorial.create_line(390, 290, 10, 290, fill='dark gray', width=2)

    canvas_tutorial.create_line(10, 50, 390, 50, fill='dark grey', width=2)
    canvas_tutorial.create_line(10, 234, 390, 234, fill='dark grey', width=2)
    canvas_tutorial.create_line(210, 95, 380, 95, fill='dark grey', width=2)
    canvas_tutorial.create_line(20, 95, 190, 95, fill='dark grey', width=2)
    # BUTTONS
    next_button = tk.Button(page, text="Next", font=("Arial", 14), width=8, height=1, command=next_element)
    next_button.place(x=283, y=243)

    back_button = tk.Button(page, text="Previous", font=("Arial", 14), width=9, height=1, command=previous_element)
    back_button.place(x=19, y=243)

    understood_button = tk.Button(page, text="Understood", font=("Arial", 14), width=9, height=1, command=understood_button_click)
    understood_button.place(x=151, y=243)
    update_tutorial_buttons()


def next_button_click():
    global next_button_click_count
    next_button_click_count += 1

def understood_button_click():
    global page
    canvas.delete("lines0")

    page.destroy()
    root.geometry(f"{width}x{height}+{og_x}+{og_y}")

    global next_button_click_count
    next_button_click_count = 0

    # The next opening starts at the first tutorial page.
    global current_index
    current_index = 0

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Coordinate Transformations")
    width = 800
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    og_x = x
    og_y = y

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg='light grey')

    canvas = tk.Canvas(root, bg='light grey', width=width, height=height)
    canvas.pack(fill='both', expand=True)

    square_size = min(width // 2, height - 63)
    square_x = width - square_size - 30
    square_y = (height - square_size) // 2
    canvas.create_rectangle(square_x, square_y, square_x + square_size, square_y + square_size, fill='white', outline='')

    grid_size = 16
    cell_size = square_size // grid_size

    for i in range(grid_size + 1):
        y = square_y + i * cell_size
        line_color = 'blue' if i == grid_size // 2 else 'gray'
        canvas.create_line(square_x, y, square_x + square_size, y, fill=line_color)

    for i in range(grid_size + 1):
        x = square_x + i * cell_size
        line_color = 'red' if i == grid_size // 2 else 'gray'
        canvas.create_line(x, square_y, x, square_y + square_size, fill=line_color)

    available_width = square_x - 10

    input_frame = tk.Frame(root, bg='light grey')
    input_frame.place(x=33, y=29)

    entry_width = 17

    font_style = ("Arial", 14, "bold")

    label_x = tk.Label(input_frame, text="x1:", bg='light grey', font=font_style)
    label_x.grid(row=0, column=0, padx=5, pady=5)

    xrangle_x = tk.Entry(input_frame, width=entry_width)
    xrangle_x.grid(row=0, column=1, padx=5, pady=5)

    label_y = tk.Label(input_frame, text="y1:", bg='light grey', font=font_style)
    label_y.grid(row=0, column=2, padx=5, pady=5)

    xrangle_y = tk.Entry(input_frame, width=entry_width)
    xrangle_y.grid(row=0, column=3, padx=5, pady=5)

    label_x2 = tk.Label(input_frame, text="x2:", bg='light grey', font=font_style)
    label_x2.grid(row=1, column=0, padx=5, pady=5)

    xrangle_x2 = tk.Entry(input_frame, width=entry_width)
    xrangle_x2.grid(row=1, column=1, padx=5, pady=5)

    label_y2 = tk.Label(input_frame, text="y2:", bg='light grey', font=font_style)
    label_y2.grid(row=1, column=2, padx=5, pady=5)

    xrangle_y2 = tk.Entry(input_frame, width=entry_width)
    xrangle_y2.grid(row=1, column=3, padx=5, pady=5)

    initial_button_width = 8.5
    initial_button_height = 1
    new_button_width = int(initial_button_width)
    new_button_height = int(initial_button_height)
    button_font_style = ("Arial", int(14 * 1.25), "bold")
    upper_bottons_font_style = ("Arial", int(12 * 1.25), "bold")
    displace_buttons_font_style = ("Arial", int(12 * 1.25), "bold")
    submit_button = tk.Button(root, text="Submit", width=new_button_width, height=new_button_height, font=upper_bottons_font_style , command=submit)

    submit_button.place(x=8, y=120+mover)

    middle_y = height // 2

    line_end_x = available_width - 20
    canvas.create_line(0, 183+mover, line_end_x, 183+mover, fill='dark gray', width=2)
    vertical_line_x = square_x - 30
    canvas.create_line(vertical_line_x, 0, vertical_line_x, height, fill='dark gray', width=2)

    rotate_label = tk.Label(root, text="   Rotations   ", bg='light grey', font=("Arial", 12, "bold"))
    rotate_label.place(x=30, y=172+mover)

    mirror = tk.Label(root, text="Transformations & Mirrors", bg='light grey', font=("Arial", 12, "bold"))
    mirror.place(x=30, y=257+mover)

    name = tk.Label(root, text=f"{MAKER}{SPACER}{NAME}", bg='lightgray', font=("Arial", 10, "bold"))
    name.place(x=15, y=350+mover)

    date = tk.Label(root, text=DATE, bg='lightgray', font=("Arial", 10, "bold"))
    date.place(x=300, y=350+mover)

    button_widths = 4
    button_height = 1

    rotate_buttons = []
    rotate_buttons_x = [30, 105, 180, 255, 330]
    rotate_buttons.append(tk.Button(root, text="-90°", width=button_widths, height=button_height, font=button_font_style, command=lambda: rotate_lines(-90)))
    rotate_buttons.append(tk.Button(root, text="90°", width=button_widths, height=button_height, font=button_font_style, command=lambda: rotate_lines(90)))
    rotate_buttons.append(tk.Button(root, text="180°", width=button_widths, height=button_height, font=button_font_style, command=lambda: rotate_lines(180)))
    rotate_buttons.append(tk.Button(root, text="270°", width=button_widths, height=button_height, font=button_font_style, command=lambda: rotate_lines(270)))
    rotate_buttons.append(tk.Button(root, text="-270°", width=button_widths, height=button_height, font=button_font_style, command=lambda: rotate_lines(-270)))

    for i in range(len(rotate_buttons)):
        rotate_buttons[i].place(x=rotate_buttons_x[i]-14, y=205+mover)

    displace_buttons = []
    displace_buttons_x = [-20, 42, 104, 178, 252, 314]
    displace_buttons.append(tk.Button(root, text="y+1", width=button_widths, height=button_height, font=displace_buttons_font_style, command=y_plus_one))
    displace_buttons.append(tk.Button(root, text="y-1", width=button_widths, height=button_height, font=displace_buttons_font_style, command=y_minus_one))
    displace_buttons.append(tk.Button(root, text="\"V\"", width=5, height=button_height, font=displace_buttons_font_style, command=mirror_lines_ony))
    displace_buttons.append(tk.Button(root, text="\"H\"", width=5, height=button_height, font=displace_buttons_font_style, command=mirror_lines_onx))
    displace_buttons.append(tk.Button(root, text="x-1", width=button_widths, height=button_height, font=displace_buttons_font_style, command=x_minus_one))
    displace_buttons.append(tk.Button(root, text="x+1", width=button_widths, height=button_height, font=displace_buttons_font_style, command=x_plus_one))

    for i in range(len(displace_buttons)):
        displace_buttons[i].place(x=displace_buttons_x[i]+26, y=291+mover)

    ##Name And Date
    canvas.create_line(0, 373+mover, 403, 373+mover, fill='dark gray', width=2)
    canvas.create_line(0, 349+mover, 403, 349+mover, fill='dark gray', width=2)
    canvas.create_line(278, 349+mover, 278, 373+mover, fill='dark gray', width=2)
    canvas.create_line(0, 269+mover, vertical_line_x, 269+mover, fill='dark gray', width=2)

    toggle_buttons_position = [120, 172, 224]
    toggle_button_texts = ["green", "yellow", "purple"]
    toggle_buttons = []
    toggle_button_width = 5
    for i in range(len(toggle_button_texts)):
        toggle_buttons.append(tk.Button(root, text=toggle_button_texts[i], width=toggle_button_width, height=button_height, font=("Arial", int(8 * 1.25 - 0.5), "bold"), command=lambda i=i: toggle_button(i)))

    for i in range(len(toggle_buttons)):
       toggle_buttons[i].place(x=toggle_buttons_position[i], y=136.3+mover)
    colors_lable = tk.Label(root, text="*Lines Colors*", bg='light grey', font=("Arial", 12, "bold"))
    colors_lable.place(x=137, y=105+mover)

    clear_button = tk.Button(root, text="Clear Lines", width=new_button_width+1, height=new_button_height, font=upper_bottons_font_style , command=clear_lines)
    clear_button.place(x=275, y=120+mover)

    points_label = tk.Label(root, text="      Points     ", bg='light grey', font=("Arial", 12, "bold"))
    canvas.create_line(0, 14, line_end_x, 14, fill='dark gray', width=2)
    points_label.place(x=30, y=2)

    draw_square_button = tk.Button(root, text="Square", width=7, height=1, font=button_font_style, command=draw_square)
    draw_square_button.place(x=680, y=355)

    tutorial = tk.Button(root, text="?", width=2, height=1, font=("Arial", int(14 * 1.25), "bold"), command=open_tutorial)
    tutorial.place(x=765, y=7)

    root.mainloop()
