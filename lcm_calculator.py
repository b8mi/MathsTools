import math
from functools import reduce

DEFAULT_NUMBERS = (6, 3, 14, 56)


def validate_numbers(numbers):
    numbers = tuple(numbers)
    if not numbers:
        raise ValueError("Supply at least one integer.")
    if any(type(number) is not int for number in numbers):
        raise ValueError("All values must be integers.")
    return numbers


def parse_numbers(raw):
    if not raw.strip():
        return list(DEFAULT_NUMBERS)
    return [int(part) for part in raw.replace(",", " ").split()]


def combine_lcm(a, b):
    divisor = math.gcd(a, b)
    return abs(a // divisor * b) if divisor else 0


def least_common_multiple(numbers):
    return reduce(combine_lcm, validate_numbers(numbers), 1)


def greatest_common_divisor(numbers):
    return reduce(math.gcd, validate_numbers(numbers), 0)


def build_lcm_steps(numbers):
    numbers = validate_numbers(numbers)
    current = abs(numbers[0])
    steps = []

    for number in numbers[1:]:
        divisor = math.gcd(current, number)
        next_value = combine_lcm(current, number)
        steps.append((current, number, divisor, next_value))
        current = next_value

    return steps


def print_steps(numbers):
    print("\nStep-by-step calculation:")
    steps = build_lcm_steps(numbers)

    if not steps:
        print(f"LCM = |{numbers[0]}| = {abs(numbers[0])}")

    for index, (a, b, divisor, result) in enumerate(steps, 1):
        if a == 0 or b == 0:
            print(f"{index}. LCM({a}, {b}) = 0")
        else:
            print(f"{index}. GCD({a}, {b}) = {divisor}")
            print(f"   LCM = |{a} × {b}| / {divisor} = {result}")

            if result == a:
                print(f"   {b} already divides the running LCM.")


def print_multiples(numbers, value):
    if value:
        print("\nCommon multiple check:")
        for number in numbers:
            print(f"{number} × {value // number} = {value}")


def display_result(numbers):
    value = least_common_multiple(numbers)
    print(f"\nLCM = {value}")
    print(f"GCD = {greatest_common_divisor(numbers)}")
    print_multiples(numbers, value)
    print_steps(numbers)


def main():
    raw = input("Integers separated by spaces [6 3 14 56]: ")
    try:
        display_result(parse_numbers(raw))
    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited.")
