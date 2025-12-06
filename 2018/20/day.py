import itertools
import sys

data = sys.stdin.read().strip()
print(data)

def draw_map(doors_h, doors_v, positions=[(0, 0)], cr=0, cc=0, rooms={}):
    min_r = min(r for r, c in itertools.chain([(cr, cc)], doors_h, doors_v, positions))
    min_c = min(c for r, c in itertools.chain([(cr, cc)], doors_h, doors_v, positions))
    max_r = max(r for r, c in itertools.chain([(cr, cc)], doors_h, doors_v, positions))+1
    max_c = max(c for r, c in itertools.chain([(cr, cc)], doors_h, doors_v, positions))+1
    print('╋' + '━━╋' * (max_c - min_c))
    for r in range(min_r, max_r):
        print(end='┃')
        for c in range(min_c, max_c):
            key = r, c
            if (r-cr, c-cc) in positions:
                room_repr = ' @'
            else:
                room_repr = f'{rooms.get(key, ''):>2}'
            print(
                room_repr,
                end=' ' if key in doors_h else '┃',
            )
        print()
        print(end='╋')
        for c in range(min_c, max_c):
            key = r, c
            print(
                '  ' if key in doors_v else '━━',
                end='╋',
            )
        print()

def go(regex, r, c):
    rooms = {(0, 0): 0}
    doors_h = set()
    doors_v = set()
    checkpoints = []
    positions = {(0, 0)}
    def update_rooms_around(r, c):
        for dr in -1, 0, 1:
            for dc in -1, 0, 1:
                update_room(r+dr, c+dc)
    def update_room(r, c):
        def update_from(nr, nc):
            value = rooms.get((nr, nc))
            if value is not None:
                value += 1
                if rooms.get((r, c), float('inf')) > value:
                    rooms[r, c] = value
                    update_rooms_around(r, c)
        if (r, c) in doors_h:
            update_from(r, c+1)
        if (r, c) in doors_v:
            update_from(r+1, c)
        if (r, c-1) in doors_h:
            update_from(r, c-1)
        if (r-1, c) in doors_v:
            update_from(r-1, c)
    def add_door(doors):
        for pr, pc in positions:
            doors.add((r+pr, c+pc))
            update_rooms_around(r+pr, c+pc)
    for idx, char in enumerate(regex):
        prev_r = r
        prev_c = c
        match char:
            case '^':
                pass
            case '$':
                pass
            case 'E':
                add_door(doors_h)
                c += 1
            case 'W':
                c -= 1
                add_door(doors_h)
            case 'S':
                add_door(doors_v)
                r += 1
            case 'N':
                r -= 1
                add_door(doors_v)
            case '(':
                endpoints = []
                checkpoints.append((r, c, positions, endpoints))
            case '|':
                r, c, positions, endpoints = checkpoints[-1]
                endpoints.append((r, c))
            case ')':
                endpoints.append((r, c))
                new_positions = set()
                r, c, positions, endpoints = checkpoints.pop()
                for pr, pc in positions:
                    for er, ec in endpoints:
                        new_position = pr + er, pc + ec
                        new_positions.add(new_position)
                positions = new_positions
                print(endpoints)
                print(new_positions)
                r = c = 0
            case _:
                raise ValueError(char)
        if char not in 'NEWS' and idx < 100:
            draw_map(doors_h, doors_v, positions, r, c, rooms=rooms)
    return doors_h, doors_v, rooms

doors_h, doors_v, rooms = go(data, 0, 0)

print('result:')
draw_map(doors_h, doors_v, rooms=rooms)

print('*** part 1:', max(rooms.values()))




print('*** part 2:', sum(v >= 1000 for v in rooms.values()))
