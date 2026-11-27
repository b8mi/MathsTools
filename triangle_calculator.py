import math
import tkinter as tk


def triangle_properties(angle_a, angle_b, base_c=1.0):
    if not all(math.isfinite(v) for v in (angle_a, angle_b, base_c)):
        raise ValueError("Enter finite numbers.")

    if angle_a <= 0 or angle_b <= 0 or angle_a + angle_b >= 180:
        raise ValueError("Angles A and B must be positive and add to less than 180°.")

    if base_c <= 0:
        raise ValueError("The reference base must be greater than zero.")

    angle_c = 180 - angle_a - angle_b
    sin_c = math.sin(math.radians(angle_c))

    side_a = base_c * math.sin(math.radians(angle_a)) / sin_c
    side_b = base_c * math.sin(math.radians(angle_b)) / sin_c

    return angle_c, side_a, side_b, base_c


def triangle_area(side_b, side_c, angle_a):
    return 0.5 * side_b * side_c * math.sin(math.radians(angle_a))


def triangle_perimeter(side_a, side_b, side_c):
    return side_a + side_b + side_c


def triangle_vertices(angle_a, side_b, base_c):
    angle = math.radians(angle_a)

    return [
        (0.0, 0.0),
        (base_c, 0.0),
        (side_b * math.cos(angle), side_b * math.sin(angle))
    ]


class TriangleApp:
    def __init__(self, root):
        self.root = root
        root.title("Triangle Calculator")
        root.geometry("760x680")
        root.minsize(530, 550)

        controls = tk.Frame(root)
        controls.pack(padx=16, pady=12)

        tk.Label(controls, text="Angle A (degrees)").grid(row=0, column=0, padx=5)
        self.angle_a = tk.Entry(controls, width=10)
        self.angle_a.grid(row=0, column=1, padx=5)
        self.angle_a.insert(0, "50")

        tk.Label(controls, text="Angle B (degrees)").grid(row=0, column=2, padx=5)
        self.angle_b = tk.Entry(controls, width=10)
        self.angle_b.grid(row=0, column=3, padx=5)
        self.angle_b.insert(0, "60")

        tk.Label(controls, text="Reference base c").grid(row=1, column=0, padx=5, pady=8)
        self.base_c = tk.Entry(controls, width=10)
        self.base_c.grid(row=1, column=1, padx=5)
        self.base_c.insert(0, "10")

        tk.Button(controls, text="Calculate & Draw", command=self.calculate).grid(row=1, column=2, padx=5)
        tk.Button(controls, text="Clear", command=self.clear).grid(row=1, column=3, padx=5)

        self.result = tk.Label(root, text="Enter two angles to calculate the third.", font=("Arial", 11))
        self.result.pack(pady=3)

        self.sides = tk.Label(root, text="")
        self.sides.pack(pady=3)

        measurements = tk.LabelFrame(root, text="Triangle Measurements", padx=20, pady=8)
        measurements.pack(padx=20, pady=8, fill="x")

        self.area_label = tk.Label(measurements, text="Area: —", font=("Arial", 12, "bold"), fg="#198754")
        self.area_label.pack(side="left", expand=True)

        self.perimeter_label = tk.Label(measurements, text="Perimeter: —", font=("Arial", 12, "bold"), fg="#2463eb")
        self.perimeter_label.pack(side="right", expand=True)

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=14)

        tk.Label(root, text="Reference length determines the triangle's actual size.").pack(pady=7)

        self.last_vertices = None
        self.last_angles = None
        self.last_sides = None

        self.canvas.bind("<Configure>", lambda event: self.draw())
        self.root.bind("<Return>", lambda event: self.calculate())

        self.calculate()

    def calculate(self):
        try:
            angle_a = float(self.angle_a.get())
            angle_b = float(self.angle_b.get())
            base = float(self.base_c.get())

            angle_c, a, b, c = triangle_properties(angle_a, angle_b, base)

            area = triangle_area(b, c, angle_a)
            perimeter = triangle_perimeter(a, b, c)

            if not all(math.isfinite(v) for v in (a, b, c, area, perimeter)):
                raise ValueError("Calculated values are too large.")

        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            self.reset_results()
            self.result.config(text=f"Invalid input: {exc}", fg="red")
            return

        self.last_vertices = triangle_vertices(angle_a, b, c)
        self.last_angles = (angle_a, angle_b, angle_c)
        self.last_sides = (a, b, c)

        self.result.config(
            text=f"A = {angle_a:.2f}°    B = {angle_b:.2f}°    C = {angle_c:.2f}°",
            fg="black"
        )

        self.sides.config(text=f"a = {a:.3f}    b = {b:.3f}    c = {c:.3f}")

        self.area_label.config(text=f"Area: {area:.3f} units²")
        self.perimeter_label.config(text=f"Perimeter: {perimeter:.3f} units")

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        if not self.last_vertices:
            return

        points = self.last_vertices
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 125 or height <= 125:
            return

        xs, ys = zip(*points)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        scale_x = (width - 125) / max(max_x - min_x, 0.001)
        scale_y = (height - 125) / max(max_y - min_y, 0.001)
        scale = min(scale_x, scale_y)

        center_x = min_x + (max_x - min_x) / 2
        center_y = min_y + (max_y - min_y) / 2

        plot = [
            (
                (x - center_x) * scale + width / 2,
                height / 2 - (y - center_y) * scale
            )
            for x, y in points
        ]

        polygon = [coordinate for point in plot for coordinate in point]
        self.canvas.create_polygon(*polygon, fill="#edf5ff", outline="")

        colors = ("#2463eb", "#198754", "#d43f3f")
        edges = ((1, 2, "a"), (0, 2, "b"), (0, 1, "c"))

        for index, (i, j, name) in enumerate(edges):
            x1, y1 = plot[i]
            x2, y2 = plot[j]

            color = colors[index]
            length = self.last_sides[index]

            self.canvas.create_line(x1, y1, x2, y2, width=3, fill=color)

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2

            self.canvas.create_text(mx, my - 13, text=f"{name} = {length:.2f}", fill=color)

        for label, angle, (x, y) in zip("ABC", self.last_angles, plot):
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="black")
            self.canvas.create_text(x, y + 20, text=f"{label} ({angle:.1f}°)", font=("Arial", 10, "bold"))

    def reset_results(self):
        self.last_vertices = None
        self.last_angles = None
        self.last_sides = None

        self.canvas.delete("all")
        self.sides.config(text="")
        self.area_label.config(text="Area: —")
        self.perimeter_label.config(text="Perimeter: —")

    def clear(self):
        for field in (self.angle_a, self.angle_b, self.base_c):
            field.delete(0, tk.END)

        self.reset_results()
        self.result.config(text="Enter two angles to calculate the third.", fg="black")


def main():
    root = tk.Tk()
    TriangleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
