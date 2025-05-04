import sys

current_key = None
total = 0

for line in sys.stdin:
    key, value = line.strip().split('\t')
    value = int(value)

    if key == current_key:
        total += value
    else:
        if current_key is not None:
            print(f"{current_key}\t{total}")
        current_key = key
        total = value

# Print the last key
if current_key is not None:
    print(f"{current_key}\t{total}")
