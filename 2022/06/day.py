import sys

data = sys.stdin.read().strip()


def solve(part_number, length):
    for i in range(len(data)):
        window = data[i-length:i]
        if len(set(window)) == length:
            print(f'*** part {part_number}:', i)
            break

solve(1, 4)
solve(2, 14)
