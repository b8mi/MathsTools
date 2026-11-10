# Python Math Projects

**MAKE MATH INTERACTIVE!** A collection of six Python projects for exploring coordinate transformations, triangles, matrices, number theory, series, and distances between lines. These started as school math projects and smaller experiments. I brought the working ideas together here, fixed calculation and input problems, and kept one version of each project instead of uploading every duplicate.

Three projects use a **Tkinter window**. The other three run in your terminal.

## Projects 

| Project | Interface | What it does |
| --- | --- | --- |
| [Coordinate Transformations](coordinate_transformations.py) | Tkinter | Draw line segments on a grid, rotate, reflect, translate, change colors, draw a square, and follow a tutorial. |
| [Triangle Angle Calculator](triangle_calculator.py) | Tkinter | Find the third angle, calculate side lengths using a reference base and the sine rule, and draw the triangle. |
| [Matrix Calculator](matrix_calculator.py) | Terminal | Add, subtract, multiply, scale, find determinants, reset, transpose, and invert matrices. |
| [Parallel Line Distance](parallel_line_distance.py) | Tkinter | Calculate the shortest distance between two parallel lines in standard form. |
| [LCM Calculator](lcm_calculator.py) | Terminal | Find the least common multiple of any list of integers. |
| [Arithmetic Series](arithmetic_series.py) | Terminal | Calculate a sum of terms of the form `a*i + b` over an inclusive integer range. |

## Setup

Install **Python 3.10 or newer**. Tkinter normally comes with Windows and macOS Python installations; some Linux distributions require a separate package such as `python3-tk`.

Download the repository and open a terminal in its folder.

```bash
pip install -r requirements.txt
```

Only the matrix project uses an external pip library (**NumPy**). The other five projects use Python's standard library.

## 1. Coordinate Transformations

Run:

```bash
python coordinate_transformations.py
```

Enter the first point (`x1`, `y1`) and second point (`x2`, `y2`), then click **Submit** to draw a line segment. Empty coordinate boxes default to zero. You can draw multiple segments and transform them together.

Features include:

- Rotate by -90°, 90°, 180°, 270°, or -270°.
- Move shapes one unit up, down, left, or right.
- Reflect over the **vertical (Y) axis** with `V`, or the **horizontal (X) axis** with `H`.
- Select green, gold, or purple for new segments; clear everything; or add a square.
- Press **?** for the illustrated, step-by-step tutorial. **Next** and **Previous** stop at the ends.

The diagram uses a fixed-size coordinate grid, so very large coordinates may fall outside the visible graph.

## 2. Triangle Angle Calculator

Run:

```bash
python triangle_calculator.py
```

Enter two angles, A and B, plus the reference base length **c** (the side connecting vertices A and B). The program finds angle C, calculates sides **a** and **b** using the sine rule, and draws a triangle that fits the window.

**Why the base length matters:** Two angles determine a triangle's *shape*, but not its absolute side lengths. The chosen base supplies the scale. All angles must be positive and add to less than 180°.

## 3. Matrix Calculator

Run:

```bash
python matrix_calculator.py
```

Enter matrices A and B, one row at a time, with numbers separated by spaces. Select a numbered operation from the menu:

- Addition and subtraction (same dimensions required).
- Matrix multiplication in either order, A × B or B × A (compatible dimensions required).
- Scalar multiplication and determinant.
- Reset either matrix without restarting the program.
- Transpose or inverse (an inverse only exists for a nonsingular square matrix).

Invalid entries can be corrected without restarting.

## 4. Parallel Line Distance

Run:

```bash
python parallel_line_distance.py
```

This program works for two parallel lines written as:

```text
A*x + B*y + C1 = 0
A*x + B*y + C2 = 0
```

It uses the distance formula:

```text
Distance = |C1 - C2| / sqrt(A² + B²)
```

A and B must be the **same for both equations** and cannot both equal zero. The result updates when you press **Calculate**. The original calculator's less-explicit yes/no input has been replaced by named coefficients.

## 5. LCM Calculator

Run:

```bash
python lcm_calculator.py
```

Enter integers separated by spaces or commas, for example:

```text
6 3 14 56
```

Result: `LCM = 168`. Press Enter without typing to use this example. This version calculates the true LCM rather than searching multiples inside a fixed range.

## 6. Arithmetic Series

Run:

```bash
python arithmetic_series.py
```

Choose the starting and ending integer, and the coefficients `a` and `b` in `a*i + b`.

The default example matches the original script: add `4*i + 2` for `i = 3` through `10`, giving **224**.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

These tests cover the numerical calculations and coordinate transformation formulas. GUI windows were also checked for startup and basic interactions, but appearance may differ across Windows, macOS, and Linux.

## About this repository

This repository collects distinct math programs from older school assignments and experiments, rather than several nearly identical drafts of the same graphing tool. See [Original File Map](docs/ORIGINAL_FILE_MAP.md) for the names of the versions that were combined and a summary of corrections.

All programs run locally. No account, cloud upload, or web service is required.
