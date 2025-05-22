import sys

INTERVALS: list[tuple[float, float, str]] = [
    (0, 49, "0-49"),
    (50, 99, "50-99"),
    (100, 199, "100-199"),
    (200, 499, "200-499"),
    (500, float("inf"), "500+")
]


def find_key(hours: str) -> str | None:
    try:
        hours = float(hours)
    except ValueError:
        return None

    for lower, upper, key in INTERVALS:
        if lower <= hours <= upper:
            return key

    return None


def main() -> None:
    for standard_input in sys.stdin:
        input_from_text_file = standard_input.strip()
        if not input_from_text_file:
            continue

        unpacked_input = input_from_text_file.split(",")
        if len(unpacked_input) != 5:
            continue

        _, _, is_recommended, hours_played, _ = unpacked_input
        key = find_key(hours_played)

        try:
            is_recommended = int(is_recommended)
        except ValueError:
            continue

        # TODO: The line below causes the final output to contain one review to little
        if key:
            print(f"{key}\t{1 if is_recommended == 1 else 0},{0 if is_recommended == 1 else 1}")


if __name__ == "__main__":
    main()
