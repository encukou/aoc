import sys

data = sys.stdin.read().splitlines()
print(data)

DIR_CHARS = {
    (-1, 0): '▲',
    (0, 1): '▶',
    (0, -1): '◀',
    (1, 0): '▼',
}

tracks = {}
cars = []
for r, line in enumerate(data):
    for c, char in enumerate(line):
        match char:
            case '\\':
                if tracks.get((r-1, c), ' ') in '│┼╭╮':
                    tracks[r, c] = '╰'
                else:
                    tracks[r, c] = '╮'
            case '/':
                if tracks.get((r-1, c), ' ') in '│┼╭╮':
                    tracks[r, c] = '╯'
                else:
                    tracks[r, c] = '╭'
            case '-':
                tracks[r, c] = '─'
            case '>':
                tracks[r, c] = '─'
                cars.append((r, c, 0, 1, 0))
            case '<':
                tracks[r, c] = '─'
                cars.append((r, c, 0, -1, 0))
            case '|':
                tracks[r, c] = '│'
            case 'v':
                tracks[r, c] = '│'
                cars.append((r, c, 1, 0, 0))
            case '^':
                tracks[r, c] = '│'
                cars.append((r, c, -1, 0, 0))
            case '+':
                tracks[r, c] = '┼'
            case ' ':
                pass
            case _:
                raise ValueError(char)

def draw_map(tracks, cars):
    cars = {(r, c): (dr, dc, m) for r, c, dr, dc, m in cars}
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if car := cars.get((r, c)):
                dr, dc, m = car
                print(end=DIR_CHARS[dr, dc])
            else:
                print(end=tracks.get((r, c), ' '))
        print(flush=True)

draw_map(tracks, cars)

def gen_crashes(tracks, cars):
    def add(r, c, dr, dc, m):
        if (r, c) in new_car_positions:
            if (r, c) not in collisions:
                collisions.append((r, c))
            new_cars[:] = [
                (pr, pc, dr, dc, m) for pr, pc, dr, dc, m in new_cars
                if (pr, pc) != (r, c)
            ]
        else:
            new_car_positions.add((r, c))
            new_cars.append((r, c, dr, dc, m))
    def turn_left():
        add(r-dc, c+dr, -dc, dr, m)
    def go_straight():
        add(r+dr, c+dc, dr, dc, m)
    def turn_right():
        add(r+dc, c-dr, dc, -dr, m)
    turn_number = 0
    while True:
        turn_number += 1
        new_cars = []
        new_car_positions = set()
        collisions = []
        for r, c, dr, dc, m in cars:
            match tracks[r, c], dr, dc, m:
                case '─', 0, _, _: go_straight()
                case '│', _, 0, _: go_straight()
                case '┼', _, _, 0:
                    m = 1
                    turn_left()
                case '┼', _, _, 1:
                    m = 2
                    go_straight()
                case '┼', _, _, 2:
                    m = 0
                    turn_right()
                case '╮', 0, _, _: turn_right()
                case '╯', 0, _, _: turn_left()
                case '╭', 0, _, _: turn_left()
                case '╰', 0, _, _: turn_right()
                case '╮', _, 0, _: turn_left()
                case '╯', _, 0, _: turn_right()
                case '╭', _, 0, _: turn_right()
                case '╰', _, 0, _: turn_left()
                case _:
                    raise ValueError((tracks[r, c], r, c, dr, dc, m))
        yield from collisions
        cars = new_cars
        if (
            turn_number < 10
            or turn_number < 100 and turn_number % 10 == 0
            or turn_number < 1000 and turn_number % 100 == 0
        ):
            print(turn_number)
            draw_map(tracks, cars)

for r, c in gen_crashes(tracks, cars.copy()):
    break
print(f'*** part 1: {c},{r}')




print('*** part 2:', ...)
