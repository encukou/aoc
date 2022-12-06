import sys

data = sys.stdin.read().strip()


def solve(part_number, length):
    for i in range(len(data)):
        if len(set(data[i:i+length])) == length:
            print(f'*** part {part_number}:', i+length)
            break

solve(1, 4)
solve(2, 14)
