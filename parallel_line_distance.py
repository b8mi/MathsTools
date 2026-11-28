import math
import tkinter as tk

BG = "#111827"
PANEL = "#1f2937"
GRID = "#293548"
AXIS = "#94a3b8"
TEXT = "#e5e7eb"
BLUE = "#60a5fa"
ORANGE = "#f97316"
GREEN = "#4ade80"


def distance_between_parallel_lines(a, b, c1, c2):
    if not all(math.isfinite(x) for x in (a, b, c1, c2)):
        raise ValueError("Enter finite numbers.")

    if a == 0 and b == 0:
        raise ValueError("At least one of A or B must be nonzero.")

    result = abs(c1 / math.hypot(a, b) - c2 / math.hypot(a, b))

    if not math.isfinite(result):
        raise ValueError("Distance exceeds the supported range.")

    return result


def perpendicular_points(a, b, c1, c2):
    distance_between_parallel_lines(a, b, c1, c2)

    norm = math.hypot(a, b)
    nx, ny = a / norm, b / norm

    p1 = (-c1 / norm * nx, -c1 / norm * ny)
    p2 = (-c2 / norm * nx, -c2 / norm * ny)

    if not all(math.isfinite(v) for point in (p1, p2) for v in point):
        raise ValueError("Coordinates exceed the supported range.")

    return p1, p2


def grid_interval(value):
    if value <= 0 or not math.isfinite(value):
        return 1

    magnitude = 10 ** math.floor(math.log10(value))
    normalized = value / magnitude

    if normalized <= 1:
        return magnitude

    if normalized <= 2:
        return 2 * magnitude

    if normalized <= 5:
        return 5 * magnitude

    return 10 * magnitude


def format_equation(a, b, c):
    return (
        f"{a:g}x "
        f"{'+' if b >= 0 else '-'} {abs(b):g}y "
        f"{'+' if c >= 0 else '-'} {abs(c):g} = 0"
    )


def clip_line(point, direction, bounds):
    px, py = point
    dx, dy = direction
    xmin, xmax, ymin, ymax = bounds

    lower = -math.inf
    upper = math.inf

    for coordinate, movement, minimum, maximum in (
        (px, dx, xmin, xmax),
        (py, dy, ymin, ymax)
    ):
        if movement == 0:
            if coordinate < minimum or coordinate > maximum:
                return None

            continue

        t1 = (minimum - coordinate) / movement
        t2 = (maximum - coordinate) / movement

        lower = max(lower, min(t1, t2))
        upper = min(upper, max(t1, t2))

        if lower > upper:
            return None

    return (
        (px + lower * dx, py + lower * dy),
        (px + upper * dx, py + upper * dy)
    )


class DistanceApp:
    def __init__(self, root):
        self.root = root
        self.values = None
        self.entries = {}
        self.zoom = 1.0
        self.scale = 1.0
        self.center = (0, 0)
        self.bounds = (-10, 10, -10, 10)
        self.graph_center = (0, 0)

        root.title("Distance Between Parallel Lines")
        root.geometry("1000x640")
        root.minsize(700, 450)
        root.configure(bg=BG)

        self.build_interface()
        self.calculate()

        root.bind("<Return>", lambda event: self.calculate())

    def build_interface(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        controls = tk.Frame(container, bg=PANEL, padx=18, pady=18)
        controls.pack(side="left", fill="y", padx=(0, 12))

        tk.Label(
            controls, text="Parallel Lines",
            font=("Arial", 18, "bold"),
            bg=PANEL, fg=TEXT
        ).pack(pady=(0, 10))

        tk.Label(
            controls,
            text="Ax + By + C₁ = 0\nAx + By + C₂ = 0",
            font=("Arial", 13),
            bg=PANEL, fg=TEXT
        ).pack(pady=(0, 16))

        inputs = tk.Frame(controls, bg=PANEL)
        inputs.pack(fill="x")

        fields = (
            ("a", "Coefficient A", "3"),
            ("b", "Coefficient B", "4"),
            ("c1", "Constant C₁", "6"),
            ("c2", "Constant C₂", "16")
        )

        for row, (key, label, initial) in enumerate(fields):
            tk.Label(
                inputs, text=label, bg=PANEL, fg=TEXT
            ).grid(row=row, column=0, sticky="w", pady=7)

            entry = tk.Entry(
                inputs, width=12, bg=BG, fg=TEXT,
                insertbackground=TEXT, relief="flat",
                font=("Arial", 12)
            )

            entry.insert(0, initial)
            entry.grid(row=row, column=1, padx=(12, 0), pady=7)

            self.entries[key] = entry

        self.make_button(
            controls, "Calculate", self.calculate, BLUE
        ).pack(fill="x", pady=(18, 5))

        self.make_button(
            controls, "Clear", self.clear, "#475569"
        ).pack(fill="x", pady=5)

        self.make_button(
            controls, "Reset View", self.reset_view, "#475569"
        ).pack(fill="x", pady=5)

        self.result = tk.Label(
            controls, text="", bg=PANEL, fg=GREEN,
            font=("Arial", 16, "bold"),
            wraplength=230
        )

        self.result.pack(pady=(20, 10))

        self.details = tk.Label(
            controls, text="", bg=PANEL, fg=TEXT,
            justify="left", wraplength=230
        )

        self.details.pack()

        graph_frame = tk.Frame(container, bg=BG)
        graph_frame.pack(side="right", fill="both", expand=True)

        toolbar = tk.Frame(graph_frame, bg=PANEL)
        toolbar.pack(fill="x")

        tk.Label(
            toolbar, text="Coordinate Graph",
            bg=PANEL, fg=TEXT,
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=12, pady=8)

        self.make_button(
            toolbar, "+", lambda: self.change_zoom(1.25), "#475569"
        ).pack(side="right", padx=4, pady=5)

        self.make_button(
            toolbar, "-", lambda: self.change_zoom(0.8), "#475569"
        ).pack(side="right", padx=4, pady=5)

        self.canvas = tk.Canvas(
            graph_frame, bg=BG,
            highlightthickness=1,
            highlightbackground=GRID
        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", lambda event: self.draw_graph())
        self.canvas.bind("<MouseWheel>", self.mouse_zoom)
        self.canvas.bind("<Button-4>", lambda event: self.change_zoom(1.25))
        self.canvas.bind("<Button-5>", lambda event: self.change_zoom(0.8))

        legend = tk.Frame(graph_frame, bg=PANEL)
        legend.pack(fill="x")

        for label, color in (
            ("Line 1", BLUE),
            ("Line 2", ORANGE),
            ("Perpendicular distance", GREEN)
        ):
            tk.Label(
                legend, text=label, fg=color,
                bg=PANEL, font=("Arial", 10, "bold")
            ).pack(side="left", padx=10, pady=10)

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat", padx=12, pady=6,
            cursor="hand2"
        )

    def calculate(self):
        try:
            values = [
                float(self.entries[key].get())
                for key in ("a", "b", "c1", "c2")
            ]

            distance = distance_between_parallel_lines(*values)
            p1, p2 = perpendicular_points(*values)

        except ValueError as error:
            self.values = None
            self.result.config(text=f"Error: {error}", fg="#f87171")
            self.details.config(text="")
            self.draw_graph()
            return

        self.values = values
        self.zoom = 1.0

        a, b, c1, c2 = values

        self.result.config(
            text=f"Distance = {distance:.6g}",
            fg=GREEN
        )

        slope = f"{-a / b:.6g}" if b != 0 else "Undefined"

        details = (
            f"Line 1:\n{format_equation(a, b, c1)}\n\n"
            f"Line 2:\n{format_equation(a, b, c2)}\n\n"
            f"Slope: {slope}\n\n"
            f"P₁ = ({p1[0]:.4g}, {p1[1]:.4g})\n"
            f"P₂ = ({p2[0]:.4g}, {p2[1]:.4g})"
        )

        if c1 == c2:
            details += "\n\nThe two lines coincide."

        self.details.config(text=details)
        self.draw_graph()

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.values = None
        self.result.config(text="")
        self.details.config(text="")
        self.zoom = 1.0

        self.draw_graph()

    def reset_view(self):
        self.zoom = 1.0
        self.draw_graph()

    def change_zoom(self, factor):
        self.zoom = max(0.1, min(10, self.zoom * factor))
        self.draw_graph()

    def mouse_zoom(self, event):
        if event.delta > 0:
            self.change_zoom(1.25)

        elif event.delta < 0:
            self.change_zoom(0.8)

    def world_to_screen(self, x, y):
        cx, cy = self.center
        gx, gy = self.graph_center

        return (
            gx + (x - cx) * self.scale,
            gy - (y - cy) * self.scale
        )

    def configure_view(self, width, height):
        margin = 28

        usable_width = max(1, width - margin * 2)
        usable_height = max(1, height - margin * 2)

        self.graph_center = (width / 2, height / 2)

        if self.values:
            a, b, c1, c2 = self.values

            p1, p2 = perpendicular_points(a, b, c1, c2)
            distance = distance_between_parallel_lines(a, b, c1, c2)

            self.center = (
                p1[0] / 2 + p2[0] / 2,
                p1[1] / 2 + p2[1] / 2
            )

            half_span = max(4, distance * 0.8)

        else:
            self.center = (0, 0)
            half_span = 5

        self.scale = (
            min(usable_width, usable_height)
            / (2 * half_span)
            * self.zoom
        )

        cx, cy = self.center

        half_width = usable_width / (2 * self.scale)
        half_height = usable_height / (2 * self.scale)

        self.bounds = (
            cx - half_width,
            cx + half_width,
            cy - half_height,
            cy + half_height
        )

    def draw_grid(self):
        xmin, xmax, ymin, ymax = self.bounds

        step = grid_interval(48 / self.scale)

        if not math.isfinite(step) or step <= 0:
            return

        start_x = math.ceil(xmin / step)
        end_x = math.floor(xmax / step)

        start_y = math.ceil(ymin / step)
        end_y = math.floor(ymax / step)

        for index in range(start_x, end_x + 1):
            value = index * step

            x1, y1 = self.world_to_screen(value, ymin)
            x2, y2 = self.world_to_screen(value, ymax)

            self.canvas.create_line(
                x1, y1, x2, y2, fill=GRID
            )

            if value != 0:
                label_y = min(ymax, max(ymin, 0))
                lx, ly = self.world_to_screen(value, label_y)

                self.canvas.create_text(
                    lx, ly + 12,
                    text=f"{value:.4g}",
                    fill=AXIS,
                    font=("Arial", 8)
                )

        for index in range(start_y, end_y + 1):
            value = index * step

            x1, y1 = self.world_to_screen(xmin, value)
            x2, y2 = self.world_to_screen(xmax, value)

            self.canvas.create_line(
                x1, y1, x2, y2, fill=GRID
            )

            if value != 0:
                label_x = min(xmax, max(xmin, 0))
                lx, ly = self.world_to_screen(label_x, value)

                self.canvas.create_text(
                    lx + 6, ly,
                    text=f"{value:.4g}",
                    fill=AXIS,
                    anchor="w",
                    font=("Arial", 8)
                )

        if ymin <= 0 <= ymax:
            x1, y1 = self.world_to_screen(xmin, 0)
            x2, y2 = self.world_to_screen(xmax, 0)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=AXIS, width=2, arrow=tk.LAST
            )

            self.canvas.create_text(
                x2 + 10, y2 - 10,
                text="X", fill=TEXT
            )

        if xmin <= 0 <= xmax:
            x1, y1 = self.world_to_screen(0, ymin)
            x2, y2 = self.world_to_screen(0, ymax)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=AXIS, width=2, arrow=tk.LAST
            )

            self.canvas.create_text(
                x2 + 12, y2 - 10,
                text="Y", fill=TEXT
            )

    def draw_parallel_line(self, a, b, c, color):
        norm = math.hypot(a, b)

        normal = (a / norm, b / norm)

        point = (
            -c / norm * normal[0],
            -c / norm * normal[1]
        )

        direction = (-normal[1], normal[0])

        segment = clip_line(point, direction, self.bounds)

        if segment is None:
            return

        first, second = segment

        x1, y1 = self.world_to_screen(*first)
        x2, y2 = self.world_to_screen(*second)

        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=3
        )

    def point_visible(self, point):
        xmin, xmax, ymin, ymax = self.bounds
        x, y = point

        return xmin <= x <= xmax and ymin <= y <= ymax

    def draw_point(self, point, color, label):
        if not self.point_visible(point):
            return

        x, y = self.world_to_screen(*point)

        self.canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5,
            fill=color, outline=TEXT
        )

        self.canvas.create_text(
            x + 13, y - 14,
            text=label, fill=color,
            font=("Arial", 10, "bold")
        )

    def draw_distance(self, a, b, c1, c2):
        p1, p2 = perpendicular_points(a, b, c1, c2)
        distance = distance_between_parallel_lines(a, b, c1, c2)

        self.draw_point(p1, BLUE, "P₁")
        self.draw_point(p2, ORANGE, "P₂")

        if distance == 0:
            x, y = self.graph_center

            self.canvas.create_text(
                x, y - 25,
                text="Coincident lines: distance = 0",
                fill=GREEN,
                font=("Arial", 12, "bold")
            )

            return

        norm = math.hypot(a, b)
        direction = (a / norm, b / norm)

        xmin, xmax, ymin, ymax = self.bounds

        clipped = clip_line(
            p1, direction, (xmin, xmax, ymin, ymax)
        )

        if clipped is None:
            return

        def projection(point):
            return (
                (point[0] - p1[0]) * direction[0]
                + (point[1] - p1[1]) * direction[1]
            )

        segment_start = min(0, projection(p2))
        segment_end = max(0, projection(p2))

        visible_start = max(segment_start, projection(clipped[0]))
        visible_end = min(segment_end, projection(clipped[1]))

        if visible_start > visible_end:
            return

        first = (
            p1[0] + direction[0] * visible_start,
            p1[1] + direction[1] * visible_start
        )

        second = (
            p1[0] + direction[0] * visible_end,
            p1[1] + direction[1] * visible_end
        )

        x1, y1 = self.world_to_screen(*first)
        x2, y2 = self.world_to_screen(*second)

        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=GREEN, width=3,
            dash=(6, 4), arrow=tk.BOTH
        )

        if self.point_visible(p1) and self.point_visible(p2):
            self.draw_right_angle(p1, p2, a, b)

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        label = self.canvas.create_text(
            mx + 16, my - 15,
            text=f"d = {distance:.6g}",
            fill=GREEN,
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        box = self.canvas.bbox(label)

        if box:
            background = self.canvas.create_rectangle(
                box[0] - 4, box[1] - 3,
                box[2] + 4, box[3] + 3,
                fill=BG, outline=""
            )

            self.canvas.tag_lower(background, label)

    def draw_right_angle(self, p1, p2, a, b):
        x1, y1 = self.world_to_screen(*p1)
        x2, y2 = self.world_to_screen(*p2)

        length = math.hypot(x2 - x1, y2 - y1)

        if length < 10:
            return

        nx = (x2 - x1) / length
        ny = (y2 - y1) / length

        tx, ty = -ny, nx

        size = min(12, length / 3)

        points = (
            x1 + nx * size,
            y1 + ny * size,
            x1 + nx * size + tx * size,
            y1 + ny * size + ty * size,
            x1 + tx * size,
            y1 + ty * size
        )

        self.canvas.create_line(
            *points, fill=GREEN, width=1.5
        )

    def draw_graph(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 60 or height < 60:
            return

        try:
            self.configure_view(width, height)
            self.draw_grid()

            if self.values is None:
                return

            a, b, c1, c2 = self.values

            self.draw_parallel_line(a, b, c1, BLUE)
            self.draw_parallel_line(a, b, c2, ORANGE)
            self.draw_distance(a, b, c1, c2)

            self.canvas.create_text(
                12, 12,
                text=f"Zoom: {self.zoom:.2f}x",
                fill=AXIS,
                anchor="nw",
                font=("Arial", 10)
            )

        except (ValueError, OverflowError, ZeroDivisionError):
            self.canvas.delete("all")

            self.canvas.create_text(
                width / 2, height / 2,
                text="Values are outside the supported graph range.",
                fill="#f87171",
                font=("Arial", 11)
            )


def main():
    root = tk.Tk()
    DistanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
