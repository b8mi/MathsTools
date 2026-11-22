  

# Python Math Projects

**MAKE MATH INTERACTIVE!** Six projects in Python for exploring coordinate transformations, triangles, matrices, number theory, series, and distances between lines. These are programs I originally wrote as school projects in maths class or as micro-experiments. I put the working concepts together in one place, fixed calculation and input errors, and kept only one copy of each project rather than uploading entire duplicates.

Three projects use a **Tkinter window**. The other three work in your terminal.

## Projects

| Project | Interface | What it does |
| --- | --- | --- |
| [Coordinate Transformations](coordinate_transformations.py) | Tkinter | Draw line segments on a grid, rotate, reflect, translate, change colors, draw a square, and go through a tutorial. |
| [Triangle Angle Calculator](triangle_calculator.py) | Tkinter | Calculate the third angle, draw the triangle, and calculate side lengths based on a reference base and the sine rule. |
| [Matrix Calculator](matrix_calculator.py) | Terminal | Add, subtract, multiply, scale, calculate determinants, reset, transpose, and invert matrices. |
| [Parallel Line Distance](parallel_line_distance.py) | Tkinter | Find the minimum distance between two parallel lines given in standard form. |
| [LCM Calculator](lcm_calculator.py) | Terminal | Calculate the least common multiple of a list of integers. |
| [Arithmetic Series](arithmetic_series.py) | Terminal | Sum a sequence of terms `a*i + b` over an inclusive integer range. |

## Setup

Ensure you have **Python 3.10 or newer** installed. Tkinter is included with most Python installations on Windows and macOS. On some Linux distros, you may have to install a package such as `python3-tk`.

Download or clone the repo and navigate to its directory in a terminal.

```bash
pip install -r requirements.txt
```

Only the matrix project uses an external pip library (**NumPy**). The remaining five projects use only the Python standard library.

## 1. Coordinate Transformations

Run:

```bash
python coordinate_transformations.py
```

Enter the first point (`x1`, `y1`) and second point (`x2`, `y2`), then click **Submit** to draw the line segment. Empty coordinate boxes default to zero. Draw as many segments as you like, and then transform them as a group.

**Features include:**

- Rotate by -90°, 90°, 180°, 270°, or -270°.
- Translate or move shapes one unit in any of the four directions.
- Reflect over the vertical (Y) axis with `V`, or the horizontal (X) axis with `H`.
- Choose green, gold, or purple for new segments; clear everything; or add a square.
- Press **?** for the illustrated, step-by-step tutorial. **Next** and **Previous** stop at the ends.

The diagram uses a coordinate grid of fixed size, so coordinates that are too big might not appear on the graph.

## 2. Triangle Angle Calculator

Run:

```bash
python triangle_calculator.py
```

Enter angles A and B and the reference base length **c** (the side between vertices A and B). The program will find angle C, calculate sides **a** and **b** using the sine rule, and draw a triangle that fits the window.

**Why the base length matters:** The size of the triangle is not uniquely determined by its angles. Any triangle with the same angles can be scaled to different sizes. The base supplies the scale. Both entered angles must be positive, and their sum must be less than 180°.

## 3. Matrix Calculator

Run:

```bash
python matrix_calculator.py
```

Enter matrices A and B, one row at a time, using spaces between numbers. Choose a numbered operation from the menu:

- Addition and subtraction (same dimensions required).
- Matrix multiplication in either order, A × B or B × A (compatible dimensions required).
- Scalar multiplication and determinant.
- Reset either matrix without restarting the program.
- Inverse or transpose (note that an inverse exists only if the matrix is square and nonsingular).

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

A and B have to be the same for both equations and cannot both equal zero. The result updates once you click **Calculate**. The old calculator's somewhat ambiguous yes/no input was replaced by named coefficients.

## 5. LCM Calculator

Run:

```bash
python lcm_calculator.py
```

Enter integers separated by spaces or commas, for example:

```text
6 3 14 56
```

Result: `LCM = 168`.

Press **Enter** without typing to use this example. This version allows you to find the exact LCM of these numbers, not just search for one within a fixed range.

## 6. Arithmetic Series

Run:

```bash
python arithmetic_series.py
```

Select the beginning and ending integers, and the coefficients `a` and `b` in `a*i + b`.

The default example matches the original script: add `4*i + 2` for `i = 3` through `10`, which gives **224**.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

These tests cover the numerical calculations and coordinate transformation formulas. GUI windows were also checked for startup and basic interactions. However, their appearance may vary between Windows, macOS, and Linux.

## About this repository

This repository is a collection of separate math programs from previous school projects and experiments, not numerous near-duplicate versions of the same graphing calculator. See [Original File Map](docs/ORIGINAL_FILE_MAP.md) for the names of the versions merged and notes on what was changed.

All programs run locally. No account needed, no uploads to the cloud, and no web services required.
