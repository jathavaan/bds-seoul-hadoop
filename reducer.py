import sys

current_key: str | None = None
sum_recommended: int = 0
sum_not_recommended: int = 0


def emit(key: str, number_of_recommended: int, number_of_not_recommended: int) -> None:
    print(f"{key},{number_of_recommended},{number_of_not_recommended}")


def main() -> None:
    global current_key, sum_recommended, sum_not_recommended

    for standard_input in sys.stdin:
        input_from_mapper = standard_input.strip("\t")
        if not input_from_mapper:
            continue

        unpacked_input = input_from_mapper.split("\t")
        if len(unpacked_input) != 2:
            continue

        key: str
        counts: str
        key, counts = unpacked_input
        counts = counts.strip()

        is_recommended, is_not_recommended = counts.split(",", 1)
        try:
            is_recommended = int(is_recommended)
            is_not_recommended = int(is_not_recommended)
        except ValueError:
            continue

        if key == current_key:
            sum_recommended += is_recommended
            sum_not_recommended += is_not_recommended
        else:
            if current_key is not None:
                emit(current_key, sum_recommended, sum_not_recommended)

            current_key = key
            sum_recommended, sum_not_recommended = is_recommended, is_not_recommended

    if current_key is not None:
        emit(current_key, sum_recommended, sum_not_recommended)


if __name__ == "__main__":
    main()
