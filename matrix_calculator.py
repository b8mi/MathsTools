import numpy as np

OPERATIONS = {
    "1": "add",
    "2": "subtract",
    "3": "multiply",
    "4": "scalar",
    "5": "determinant",
    "7": "transpose",
    "8": "inverse",
    "9": "rref"
}


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
        except ValueError:
            pass
        print("Enter a whole number greater than 0.")


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if np.isfinite(value):
                return value
        except ValueError:
            pass
        print("Enter a finite number.")


def parse_row(raw, cols):
    row = [float(x) for x in raw.split()]
    if len(row) != cols or not all(np.isfinite(row)):
        raise ValueError(f"Enter exactly {cols} valid numbers.")
    return row


def input_matrix(name):
    rows = read_positive_int(f"Enter the rows in matrix {name}: ")
    cols = read_positive_int(f"Enter the columns in matrix {name}: ")
    values = []

    for i in range(rows):
        while True:
            raw = input(f"{name}, row {i + 1} ({cols} numbers): ")
            try:
                values.append(parse_row(raw, cols))
                break
            except ValueError:
                print(f"Enter exactly {cols} valid numbers.")

    return np.array(values, dtype=float)


def require_matching(a, b):
    if b is None or a.shape != b.shape:
        raise ValueError("Matrices must have matching dimensions.")


def require_square(a):
    if a.shape[0] != a.shape[1]:
        raise ValueError("The matrix must be square.")


def row_reduce(matrix, tolerance=1e-10):
    result = np.array(matrix, dtype=float, copy=True)
    rows, cols = result.shape
    pivot_row = 0
    pivot_columns = []
    scale = np.max(np.abs(result)) if result.size else 0

    if not scale:
        return result, pivot_columns

    result /= scale

    for col in range(cols):
        if pivot_row == rows:
            break

        candidate = pivot_row + np.argmax(np.abs(result[pivot_row:, col]))

        if abs(result[candidate, col]) <= tolerance:
            continue

        result[[pivot_row, candidate]] = result[[candidate, pivot_row]]
        result[pivot_row] /= result[pivot_row, col]

        for row in range(rows):
            if row != pivot_row:
                factor = result[row, col]
                result[row] -= factor * result[pivot_row]
                result[row, col] = 0.0

        pivot_columns.append(col)
        pivot_row += 1

    result[np.abs(result) <= tolerance] = 0.0
    return result, pivot_columns


def calculate(operation, a, b=None, scalar=None):
    if operation in ("add", "subtract"):
        require_matching(a, b)
        return a + b if operation == "add" else a - b

    if operation == "multiply":
        if b is None or a.shape[1] != b.shape[0]:
            raise ValueError("Columns of A must equal rows of B.")
        return a @ b

    if operation == "scalar":
        return a * scalar

    if operation in ("determinant", "inverse"):
        require_square(a)

        if operation == "determinant":
            return float(np.linalg.det(a))

        try:
            return np.linalg.inv(a)
        except np.linalg.LinAlgError as exc:
            raise ValueError("The matrix is singular and has no inverse.") from exc

    if operation == "transpose":
        return a.T

    if operation == "rref":
        return row_reduce(a)[0]

    raise ValueError("Unknown operation.")


def print_matrix(value):
    if isinstance(value, np.ndarray):
        print(np.array2string(value, precision=4, suppress_small=True))
    else:
        print(f"{value:.6g}")


class MatrixCalculator:

    def __init__(self, a, b):
        self.matrices = {"A": a, "B": b}

    def choose_matrix(self):
        while True:
            name = input("Choose A or B: ").strip().upper()
            if name in self.matrices:
                return name, self.matrices[name]
            print("Please enter A or B.")

    def show_matrices(self):
        for name, matrix in self.matrices.items():
            rows, cols = matrix.shape
            print(f"\n{name} ({rows} × {cols}) =")
            print_matrix(matrix)

    def show_menu(self):
        print("\n1 Add  2 Subtract  3 Multiply")
        print("4 Scalar  5 Determinant  6 Reset matrix")
        print("7 Transpose  8 Inverse  9 RREF")
        print("0 Exit")

    def reset_matrix(self):
        name, _ = self.choose_matrix()
        self.matrices[name] = input_matrix(name)
        print(f"Matrix {name} updated.")

    def multiply(self):
        while True:
            order = input("Multiply A*B or B*A? [1/2]: ").strip()
            if order in ("1", "2"):
                break
            print("Choose 1 or 2.")

        first, second = ("A", "B") if order == "1" else ("B", "A")
        return calculate("multiply", self.matrices[first], self.matrices[second])

    def perform_operation(self, choice):
        operation = OPERATIONS[choice]

        if operation in ("add", "subtract"):
            return calculate(operation, self.matrices["A"], self.matrices["B"])

        if operation == "multiply":
            return self.multiply()

        _, chosen = self.choose_matrix()

        if operation == "rref":
            result, pivots = row_reduce(chosen)
            pivot_text = ", ".join(str(p + 1) for p in pivots)
            print(f"\nNumerical rank: {len(pivots)}")
            print(f"Pivot columns: {pivot_text or 'None'}")
            return result

        scalar = read_float("Scalar: ") if operation == "scalar" else None
        return calculate(operation, chosen, scalar=scalar)

    def store_result(self, result):
        if not isinstance(result, np.ndarray):
            return

        if not np.all(np.isfinite(result)):
            print("Result contains non-finite values and cannot be stored.")
            return

        while True:
            name = input("Save result to A or B? [Enter to skip]: ").strip().upper()

            if not name:
                return

            if name in self.matrices:
                self.matrices[name] = result.copy()
                print(f"Result saved to matrix {name}.")
                return

            print("Enter A, B, or press Enter to skip.")

    def run(self):
        while True:
            self.show_matrices()
            self.show_menu()
            choice = input("Choice: ").strip()

            if choice == "0":
                print("Goodbye!")
                break

            if choice == "6":
                self.reset_matrix()
                continue

            if choice not in OPERATIONS:
                print("Unknown choice.")
                continue

            try:
                result = self.perform_operation(choice)
                print("\nResult:")
                print_matrix(result)

                if isinstance(result, np.ndarray):
                    self.store_result(result)
                else:
                    input("\nPress Enter to continue...")

            except (ValueError, np.linalg.LinAlgError) as exc:
                print(f"Error: {exc}")
                input("\nPress Enter to continue...")


def main():
    print("\nMATRIX CALCULATOR")
    print("Enter both matrices. Either one can be changed later.")
    a = input_matrix("A")
    b = input_matrix("B")
    calculator = MatrixCalculator(a, b)
    calculator.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited.")
