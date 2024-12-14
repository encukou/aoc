import dataclasses
import sys

data = sys.stdin.read()
try:
    data1, data2 = data.split('***')
except ValueError:
    data1 = data2 = data.splitlines()
else:
    data1 = data1.strip().splitlines()
    data2 = data2.strip().splitlines()
print(data1)
print(data2)

DIR_CHARS = {
    (-1, 0): '▲',
    (0, 1): '▶',
    (0, -1): '◀',
    (1, 0): '▼',
}

@dataclasses.dataclass
class Cart:
    r: int
    c: int
    dr: int
    dc: int
    mem: int
    dead = False

    def pos(self):
        return self.r, self.c

def parse_data(data):
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
                    cars.append(Cart(r, c, 0, 1, 0))
                case '<':
                    tracks[r, c] = '─'
                    cars.append(Cart(r, c, 0, -1, 0))
                case '|':
                    tracks[r, c] = '│'
                case 'v':
                    tracks[r, c] = '│'
                    cars.append(Cart(r, c, 1, 0, 0))
                case '^':
                    tracks[r, c] = '│'
                    cars.append(Cart(r, c, -1, 0, 0))
                case '+':
                    tracks[r, c] = '┼'
                case ' ':
                    pass
                case _:
                    raise ValueError(char)
    return tracks, cars

def draw_map(tracks, cars):
    cars = {(car.r, car.c): car for car in cars}
    for r, row in enumerate(data2):
        for c, char in enumerate(data1[0]):
            if car := cars.get((r, c)):
                print(end=DIR_CHARS[car.dr, car.dc])
            else:
                print(end=tracks.get((r, c), ' '))
        print(flush=True)

def gen_crashes(tracks, cars):
    def go_straight(car):
        car.r += car.dr
        car.c += car.dc
        assert (car.dr*car.dc==0 and abs(car.dr+car.dc)==1), car
        for other in cars:
            if other is not car and other.pos() == car.pos() and not other.dead:
                car.dead = True
                other.dead = True
                collisions.append((car.r, car.c))
    def turn_left(car):
        car.dr, car.dc = -car.dc, car.dr
        go_straight(car)
    def turn_right(car):
        car.dr, car.dc = car.dc, -car.dr
        go_straight(car)
    turn_number = 0
    draw_map(tracks, cars)
    while True:
        collisions = []
        cars.sort(key=Cart.pos)
        for car in cars:
            if car.dead:
                continue
            match tracks[car.r, car.c], car.dr, car.dc, car.mem:
                case '─', 0, _, _: go_straight(car)
                case '│', _, 0, _: go_straight(car)
                case '┼', _, _, 0:
                    car.mem = 1
                    turn_left(car)
                case '┼', _, _, 1:
                    car.mem = 2
                    go_straight(car)
                case '┼', _, _, 2:
                    car.mem = 0
                    turn_right(car)
                case '╮', 0, _, _: turn_right(car)
                case '╯', 0, _, _: turn_left(car)
                case '╭', 0, _, _: turn_left(car)
                case '╰', 0, _, _: turn_right(car)
                case '╮', _, 0, _: turn_left(car)
                case '╯', _, 0, _: turn_right(car)
                case '╭', _, 0, _: turn_right(car)
                case '╰', _, 0, _: turn_left(car)
                case _:
                    raise ValueError((tracks[car.r, car.c], car))
        if (
            turn_number < 20
            or turn_number < 100 and turn_number % 10 == 0
            or turn_number < 1000 and turn_number % 100 == 0
        ):
            print(turn_number)
            draw_map(tracks, cars)
        cars = [c for c in cars if not c.dead]
        yield collisions, cars
        turn_number += 1

for collisions, cars in gen_crashes(*parse_data(data1)):
    if collisions:
        for r, c in collisions:
            break
        break
print(f'*** part 1: {c},{r}')

for i, (collisions, cars) in enumerate(gen_crashes(*parse_data(data2))):
    if collisions:
        for r, c in collisions:
            print(f'{i}: Boom! @ {r},{c}')
        print(f'... {len(cars)} left')
    if len(cars) == 1:
        r, c = cars[0].pos()
        break

print(f'*** part 2: {c},{r}')
