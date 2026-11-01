def sum_linear_terms(start, stop, slope=4, intercept=2):
    if start > stop:
        raise ValueError("Start must be less than or equal to stop.")
    return sum(slope * i + intercept for i in range(start, stop + 1))


def ask_int(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    return int(raw) if raw else default


def main():
    print("SUM OF LINEAR TERMS: a*i + b")
    try:
        start = ask_int("Start (inclusive)", 3)
        stop = ask_int("End (inclusive)", 10)
        slope = ask_int("Coefficient a", 4)
        intercept = ask_int("Constant b", 2)
        total = sum_linear_terms(start, stop, slope, intercept)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return
    print(f"Sum of ({slope}i + {intercept}) for i = {start} through {stop}: {total}")


if __name__ == "__main__":
    main()
