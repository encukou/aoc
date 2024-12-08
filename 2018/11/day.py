import sys

data = sys.stdin.read()
print(data)

serial = int(data)

def get_power(x, y, serial):
    rack = x + 10
    power = rack * y + serial
    power *= rack
    power = (power // 100) % 10 - 5
    return power

assert get_power(3, 5, 8) == 4, get_power(3, 5, 8) 
assert get_power(122, 79, 57) == -5, get_power(122, 79, 57) 
assert get_power(217,196, 39) == 0
assert get_power(101,153, 71) == 4


grid = {}
for x in range(1, 300+1):
    for y in range(1, 300+1):
        power = get_power(x, y, serial)
        print(end=f'{power:+} ')
        grid[x, y] = power
    print()

maximum = -1000
for x in range(1, 300+1-3):
    for y in range(1, 300+1-3):
        square_total = 0
        for xx in range(3):
            for yy in range(3):
                square_total += grid[x+xx, y+yy]
        if square_total > maximum:
            maximum = square_total
            best_coords = x, y

x, y = best_coords
print(f'{x},{y} : {maximum}')

print('*** part 1:', f'{x},{y}')




print('*** part 2:', ...)
