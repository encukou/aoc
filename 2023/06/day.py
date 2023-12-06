import sys
from math import prod

data = sys.stdin.read().splitlines()
print(data)

def numbers_from_line(line):
    header, num_part = line.split(':')
    return [int(n) for n in num_part.split()]

def solve(time, record):
    print('---', time, record)

    def is_win(held):
        "Do I win if I hold for this long?"
        released = time - held
        distance = held * released
        return distance > record

    # Find the first winning time X
    low, high = 0, time // 2
    while low != high - 1:
        mid = (low + high) // 2
        if is_win(mid):
            high = mid
        else:
            low = mid
        print([low, high])

    # Times smaller than X, and larger than (time-X), don't win.
    # Everything in between does
    return time - low - high

results = [
    solve(time, record) for time, record in zip(
        numbers_from_line(data[0]),
        numbers_from_line(data[1]),
    )
]
print(results)

print('*** part 1:', prod(results))

result = solve(
    *numbers_from_line(data[0].replace(' ', '')),
    *numbers_from_line(data[1].replace(' ', '')),
)

print('*** part 2:', result)
