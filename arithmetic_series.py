
from fractions import Fraction


def validate_range(start, stop):
    if start > stop:
        raise ValueError("Start must be less than or equal to stop.")


def term_count(start, stop):
    validate_range(start, stop)
    return stop - start + 1


def linear_term(index, slope=4, intercept=2):
    return slope * index + intercept


def sum_linear_terms(start, stop, slope=4, intercept=2):
    count = term_count(start, stop)
    first = linear_term(start, slope, intercept)
    last = linear_term(stop, slope, intercept)
    return count * (first + last) // 2


def ask_int(prompt, default):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        try:
            return int(raw) if raw else default
        except ValueError:
            print("Please enter a whole number.")


def ask_parameters():
    start = ask_int("Start (inclusive)", 3)
    stop = ask_int("End (inclusive)", 10)

    while stop < start:
        print("End cannot be smaller than start.")
        stop = ask_int("End (inclusive)", start)

    slope = ask_int("Coefficient a", 4)
    intercept = ask_int("Constant b", 2)
    return start, stop, slope, intercept


def format_expression(slope, intercept):
    sign = "+" if intercept >= 0 else "-"
    return f"{slope}i {sign} {abs(intercept)}"


def sequence_direction(count, slope):
    if count == 1 or slope == 0:
        return "Constant"
    return "Increasing" if slope > 0 else "Decreasing"


def analyze_sequence(start, stop, slope=4, intercept=2):
    count = term_count(start, stop)
    first = linear_term(start, slope, intercept)
    last = linear_term(stop, slope, intercept)
    total = sum_linear_terms(start, stop, slope, intercept)

    return {
        "Term count": count,
        "First term": first,
        "Last term": last,
        "Minimum": min(first, last),
        "Maximum": max(first, last),
        "Mean (exact)": Fraction(total, count),
        "Common difference": slope,
        "Trend": sequence_direction(count, slope),
        "Sum": total
    }


def preview_indices(start, stop, limit=12):
    count = term_count(start, stop)

    if limit < 2:
        raise ValueError("Preview limit must be at least 2.")

    if count <= limit:
        yield from range(start, stop + 1)
        return

    head = limit // 2
    tail = limit - head

    yield from range(start, start + head)
    yield None
    yield from range(stop - tail + 1, stop + 1)


def cumulative_rows(start, stop, slope=4, intercept=2, limit=12):
    for index in preview_indices(start, stop, limit):
        if index is None:
            yield None
        else:
            term = linear_term(index, slope, intercept)
            running_sum = sum_linear_terms(start, index, slope, intercept)
            yield index, term, running_sum


def calculate_column_widths(headers, rows):
    valid_rows = [row for row in rows if row is not None]
    return [max(len(headers[i]), *(len(str(row[i])) for row in valid_rows)) for i in range(len(headers))]


def print_term_table(start, stop, slope, intercept):
    rows = list(cumulative_rows(start, stop, slope, intercept))
    headers = ("Index", "Term", "Running sum")
    widths = calculate_column_widths(headers, rows)
    template = "  ".join("{:>" + str(w) + "}" for w in widths)

    print("\nTERM BREAKDOWN")
    print(template.format(*headers))
    print("-" * (sum(widths) + 4))

    for row in rows:
        if row is None:
            print(template.format("...", "...", "..."))
        else:
            print(template.format(*row))


def print_analysis(start, stop, slope, intercept):
    print("\nSEQUENCE ANALYSIS")
    analysis = analyze_sequence(start, stop, slope, intercept)

    for label, value in analysis.items():
        print(f"  {label:<20}: {value}")

    print("  Formula: n × (first + last) / 2")


def main():
    print("SUM OF LINEAR TERMS: a*i + b")

    try:
        start, stop, slope, intercept = ask_parameters()
        total = sum_linear_terms(start, stop, slope, intercept)
        expression = format_expression(slope, intercept)

        print(f"\nSum of ({expression}) for i = {start} through {stop}: {total}")
        print_analysis(start, stop, slope, intercept)
        print_term_table(start, stop, slope, intercept)

    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")


if __name__ == "__main__":
    main()
