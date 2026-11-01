import math


def least_common_multiple(numbers):
    if not numbers:
        raise ValueError("Supply at least one integer.")
    result = 1
    for number in numbers:
        if not isinstance(number, int):
            raise ValueError("All values must be integers.")
        if number == 0:
            return 0
        # Dividing by the GCD avoids searching an arbitrary range of multiples.
        result = result // math.gcd(result, number) * abs(number)
    return result


def main():
    raw = input("Integers separated by spaces [6 3 14 56]: ").strip()
    try:
        numbers = [int(x) for x in raw.replace(",", " ").split()] if raw else [6, 3, 14, 56]
        value = least_common_multiple(numbers)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    print(f"LCM = {value}")
    if value:
        for number in numbers:
            print(f"{number} × {value // number} = {value}")


if __name__ == "__main__":
    main()
