import numpy as np


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
        except ValueError:
            pass
        print("Enter a positive whole number.")


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if np.isfinite(value):
                return value
        except ValueError:
            pass
        print("Enter a finite number.")


def input_matrix(name):
    rows = read_positive_int(f"Rows in matrix {name}: ")
    cols = read_positive_int(f"Columns in matrix {name}: ")
    values = []
    for i in range(rows):
        while True:
            raw = input(f"{name}, row {i + 1} ({cols} numbers separated by spaces): ").split()
            try:
                row = [float(x) for x in raw]
            except ValueError:
                row = []
            if len(row) == cols and all(np.isfinite(row)):
                values.append(row)
                break
            print(f"Enter exactly {cols} valid numbers, separated by spaces.")
    return np.array(values, dtype=float)


def calculate(operation, a, b=None, scalar=None):
    if operation in ("add", "subtract"):
        if b is None or a.shape != b.shape:
            raise ValueError("Matrices must have matching dimensions.")
        return a + b if operation == "add" else a - b
    if operation == "multiply":
        if b is None or a.shape[1] != b.shape[0]:
            raise ValueError("Columns of the first matrix must equal rows of the second.")
        return a @ b
    if operation == "scalar":
        return a * scalar
    if operation in ("determinant", "inverse"):
        if a.shape[0] != a.shape[1]:
            raise ValueError("The matrix must be square.")
        if operation == "determinant":
            return float(np.linalg.det(a))
        try:
            return np.linalg.inv(a)
        except np.linalg.LinAlgError as exc:
            raise ValueError("The matrix is singular and has no inverse.") from exc
    if operation == "transpose":
        return a.T
    raise ValueError("Unknown operation.")


def print_matrix(value):
    if isinstance(value, np.ndarray):
        print(np.array2string(value, precision=4, suppress_small=True))
    else:
        print(f"{value:.6g}")


def choose_matrix(a, b):
    while True:
        choice = input("Choose A or B: ").strip().upper()
        if choice == "A":
            return choice, a
        if choice == "B":
            return choice, b
        print("Please enter A or B.")


def main():
    print("\nMATRIX CALCULATOR")
    print("Enter the values for two matrices. You can change either one later.")
    a = input_matrix("A")
    b = input_matrix("B")
    while True:
        print("\nA =")
        print_matrix(a)
        print("B =")
        print_matrix(b)
        print("\n1 Add  2 Subtract  3 Multiply  4 Scalar  5 Determinant")
        print("6 Reset a matrix  7 Transpose  8 Inverse  0 Exit")
        choice = input("Choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        try:
            if choice in ("1", "2"):
                result = calculate("add" if choice == "1" else "subtract", a, b)
            elif choice == "3":
                order = input("Multiply A*B or B*A? [1/2]: ").strip()
                if order not in ("1", "2"):
                    print("Choose 1 or 2.")
                    continue
                result = calculate("multiply", a, b) if order == "1" else calculate("multiply", b, a)
            elif choice in ("4", "5", "7", "8"):
                name, chosen = choose_matrix(a, b)
                operation = {"4": "scalar", "5": "determinant", "7": "transpose", "8": "inverse"}[choice]
                scalar = read_float("Scalar: ") if choice == "4" else None
                result = calculate(operation, chosen, scalar=scalar)
            elif choice == "6":
                name, _ = choose_matrix(a, b)
                replacement = input_matrix(name)
                if name == "A":
                    a = replacement
                else:
                    b = replacement
                print(f"Matrix {name} updated.")
                continue
            else:
                print("Unknown choice.")
                continue
            print("\nResult:")
            print_matrix(result)
        except ValueError as exc:
            print(f"Error: {exc}")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited.")
