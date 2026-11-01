import math
import tkinter as tk
from tkinter import messagebox


def triangle_properties(angle_a, angle_b, base_c=1.0):
    values = (angle_a, angle_b, base_c)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Enter finite numbers.")
    if angle_a <= 0 or angle_b <= 0 or angle_a + angle_b >= 180:
        raise ValueError("Angles A and B must be positive and add to less than 180°.")
    if base_c <= 0:
        raise ValueError("The reference base must be greater than zero.")
    angle_c = 180 - angle_a - angle_b
    # Sine rule: a/sin(A) = b/sin(B) = c/sin(C).
    sin_c = math.sin(math.radians(angle_c))
    side_a = base_c * math.sin(math.radians(angle_a)) / sin_c
    side_b = base_c * math.sin(math.radians(angle_b)) / sin_c
    return angle_c, side_a, side_b, base_c


def triangle_vertices(angle_a, side_b, base_c):
    angle = math.radians(angle_a)
    return [(0.0, 0.0), (base_c, 0.0),
            (side_b * math.cos(angle), side_b * math.sin(angle))]


class TriangleApp:
    def __init__(self, root):
        self.root = root
        root.title("Triangle Angle Calculator")
        root.geometry("760x630")
        root.minsize(530, 500)
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
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=14)
        tk.Label(root, text="Reference length determines size; two angles alone determine only the triangle's shape.").pack(pady=7)
        self.last_vertices = None
        self.last_angles = None
        self.last_sides = None
        self.canvas.bind("<Configure>", lambda event: self.draw())
        self.calculate()

    def calculate(self):
        try:
            a_angle = float(self.angle_a.get())
            b_angle = float(self.angle_b.get())
            base = float(self.base_c.get())
            c_angle, a, b, c = triangle_properties(a_angle, b_angle, base)
        except ValueError as exc:
            self.last_vertices = None
            self.canvas.delete("all")
            self.result.config(text=f"Invalid input: {exc}", fg="red")
            self.sides.config(text="")
            return
        self.last_vertices = triangle_vertices(a_angle, b, c)
        self.last_angles = (a_angle, b_angle, c_angle)
        self.last_sides = (a, b, c)
        self.result.config(text=f"A = {a_angle:.2f}°    B = {b_angle:.2f}°    C = {c_angle:.2f}°", fg="black")
        self.sides.config(text=f"a = {a:.3f}    b = {b:.3f}    c = {c:.3f}")
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if not self.last_vertices:
            return
        points = self.last_vertices
        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        if width <= 100 or height <= 100:
            return
        xs, ys = zip(*points)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        scale = min((width - 125) / max(max_x - min_x, 0.001),
                    (height - 125) / max(max_y - min_y, 0.001))
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        plot = [((x - center_x) * scale + width / 2,
                 height / 2 - (y - center_y) * scale) for x, y in points]
        colors = ("#2463eb", "#198754", "#d43f3f")
        for i, j, color, name in ((1, 2, colors[0], "a"),
                                  (0, 2, colors[1], "b"),
                                  (0, 1, colors[2], "c")):
            x1, y1 = plot[i]
            x2, y2 = plot[j]
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill=color)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my - 13, text=f"{name} = {self.last_sides['abc'.index(name)]:.2f}", fill=color)
        for label, angle, (x, y) in zip("ABC", self.last_angles, plot):
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="black")
            self.canvas.create_text(x, y + 20, text=f"{label} ({angle:.1f}°)", font=("Arial", 10, "bold"))

    def clear(self):
        for field in (self.angle_a, self.angle_b, self.base_c):
            field.delete(0, tk.END)
        self.last_vertices = None
        self.canvas.delete("all")
        self.result.config(text="Enter two angles to calculate the third.", fg="black")
        self.sides.config(text="")


def main():
    root = tk.Tk()
    TriangleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
