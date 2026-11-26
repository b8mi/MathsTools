
from fractions import Fraction
from decimal import Decimal, localcontext


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


def sequence_median(start, stop, slope=4, intercept=2):
    validate_range(start, stop)

    first = linear_term(start, slope, intercept)
    last = linear_term(stop, slope, intercept)

    return Fraction(first + last, 2)


def sequence_variance(start, stop, slope=4):
    count = term_count(start, stop)

    return Fraction(slope ** 2 * (count ** 2 - 1), 12)


def sequence_standard_deviation(start, stop, slope=4):
    variance = sequence_variance(start, stop, slope)

    with localcontext() as context:
        context.prec = 16
        value = Decimal(variance.numerator) / Decimal(variance.denominator)
        return value.sqrt()


def find_term_indices(value, start, stop, slope=4, intercept=2):
    validate_range(start, stop)

    if slope == 0:
        return (start, stop) if value == intercept else None

    index = Fraction(value - intercept, slope)

    if index.denominator != 1:
        return None

    index = int(index)

    if start <= index <= stop:
        return index, index

    return None


def format_term_location(location):
    if location is None:
        return "Not present"

    first, last = location

    if first == last:
        return f"i = {first}"

    return f"Every index from {first} to {last}"


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
    if slope == 0:
        return str(intercept)

    if slope == 1:
        expression = "i"

    elif slope == -1:
        expression = "-i"

    else:
        expression = f"{slope}i"

    if intercept == 0:
        return expression

    sign = "+" if intercept > 0 else "-"

    return f"{expression} {sign} {abs(intercept)}"


def sequence_direction(count, slope):
    if count == 1 or slope == 0:
        return "Constant"

    return "Increasing" if slope > 0 else "Decreasing"


def analyze_sequence(start, stop, slope=4, intercept=2):
    count = term_count(start, stop)
    first = linear_term(start, slope, intercept)
    last = linear_term(stop, slope, intercept)
    total = sum_linear_terms(start, stop, slope, intercept)

    minimum = min(first, last)
    maximum = max(first, last)
    variance = sequence_variance(start, stop, slope)
    deviation = sequence_standard_deviation(start, stop, slope)
    zero_location = find_term_indices(0, start, stop, slope, intercept)

    return {
        "Term count": count,
        "First term": first,
        "Last term": last,
        "Minimum": minimum,
        "Maximum": maximum,
        "Range": maximum - minimum,
        "Mean (exact)": Fraction(total, count),
        "Median (exact)": sequence_median(start, stop, slope, intercept),
        "Variance (exact)": variance,
        "Standard deviation": f"{deviation:.8g}",
        "Common difference": slope,
        "Trend": sequence_direction(count, slope),
        "Zero term": format_term_location(zero_location),
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

    widths = []

    for index, header in enumerate(headers):
        lengths = [len(header)]
        lengths.extend(len(str(row[index])) for row in valid_rows)
        widths.append(max(lengths))

    return widths


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
    label_width = max(len(label) for label in analysis)

    for label, value in analysis.items():
        print(f"  {label:<{label_width}} : {value}")

    print("\n  Sum formula: n × (first + last) / 2")
    print("  Variance formula: a² × (n² - 1) / 12")


def search_sequence(start, stop, slope, intercept):
    print("\nTERM SEARCH")
    print("Enter a term to find its index, or press Enter to exit.")

    while True:
        try:
            raw = input("Search: ").strip()

        except EOFError:
            return

        if not raw:
            return

        try:
            value = int(raw)

        except ValueError:
            print("Please enter a whole number.")
            continue

        location = find_term_indices(value, start, stop, slope, intercept)

        if location is None:
            print(f"{value} does not exist in this sequence.")

        else:
            print(f"{value} found at {format_term_location(location)}.")


def main():
    print("SUM OF LINEAR TERMS: a*i + b")

    try:
        start, stop, slope, intercept = ask_parameters()

        total = sum_linear_terms(start, stop, slope, intercept)
        expression = format_expression(slope, intercept)

        print(f"\nSum of ({expression}) for i = {start} through {stop}: {total}")

        print_analysis(start, stop, slope, intercept)
        print_term_table(start, stop, slope, intercept)
        search_sequence(start, stop, slope, intercept)

    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")


if __name__ == "__main__":
    main()
