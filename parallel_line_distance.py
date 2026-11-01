import math
import tkinter as tk


def distance_between_parallel_lines(a, b, c1, c2):
    if not all(math.isfinite(x) for x in (a, b, c1, c2)):
        raise ValueError("Enter finite numbers.")
    if a == 0 and b == 0:
        raise ValueError("At least one of A or B must be nonzero.")
    return abs(c1 - c2) / math.hypot(a, b)


class DistanceApp:
    def __init__(self, root):
        root.title("Distance Between Parallel Lines")
        frame = tk.Frame(root, padx=20, pady=18)
        frame.pack()
        tk.Label(frame, text="For Ax + By + C₁ = 0 and Ax + By + C₂ = 0", font=("Arial", 11, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 13))
        self.entries = {}
        for row, (key, label, initial) in enumerate((
            ("a", "Shared coefficient A", "3"),
            ("b", "Shared coefficient B", "4"),
            ("c1", "Constant C₁", "6"),
            ("c2", "Constant C₂", "16"),
        ), start=1):
            tk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=4)
            entry = tk.Entry(frame, width=16)
            entry.insert(0, initial)
            entry.grid(row=row, column=1, pady=4, padx=(8, 0))
            self.entries[key] = entry
        tk.Button(frame, text="Calculate", command=self.calculate).grid(row=5, column=0, pady=12)
        tk.Button(frame, text="Clear", command=self.clear).grid(row=5, column=1, pady=12)
        self.result = tk.Label(frame, text="", font=("Arial", 12))
        self.result.grid(row=6, column=0, columnspan=2, pady=7)
        self.calculate()

    def calculate(self):
        try:
            values = [float(self.entries[key].get()) for key in ("a", "b", "c1", "c2")]
            result = distance_between_parallel_lines(*values)
        except ValueError as exc:
            self.result.config(text=f"Error: {exc}", fg="red")
            return
        self.result.config(text=f"Distance = {result:.6g}", fg="black")

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result.config(text="")


def main():
    root = tk.Tk()
    DistanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
