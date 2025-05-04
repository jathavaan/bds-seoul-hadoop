import sys
import csv

reader = csv.reader(sys.stdin)
header = next(reader, None)  # skip header

for row in reader:
    try:
        origin = row[21]  # "Origin" is at index 21
        if origin:
            print(f"{origin}\t1")
    except IndexError:
        continue  # skip malformed rows
