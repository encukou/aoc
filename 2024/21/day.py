import collections
from functools import cache
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
}

class Keyboard:
    def __init__(self, *buttons):
        self.buttons = buttons
        coords = {}
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char != ' ':
                    coords[char] = r, c
        self.coords = coords
        self.paths = {}

    def get_paths(self, a, b):
        try:
            path = self.paths[a, b]
        except KeyError:
            self.init_paths_from(a)
            path = self.paths[a, b]
            print(f'{a!r}→{b!r}: {path!r}')
        return path

    def init_paths_from(self, a):
        print(f'Finding paths from {a} in {self.buttons}')
        char_coords = {p: c for c, p in self.coords.items()}
        r, c = self.coords[a]
        heads = collections.deque([(r, c, '')])
        while heads:
            r, c, path = heads.popleft()
            pos = r, c
            b = char_coords.get(pos)
            if b is None:
                continue
            paths = self.paths.setdefault((a, b), [])
            path_A = path + 'A'
            if paths and len(paths[0]) <= len(path):
                continue
            paths.append(path_A)
            print(f' - {a!r}→{b!r}: {path_A!r}')
            for char, (dr, dc) in DIRS.items():
                if char in path.rstrip(char):
                    continue
                heads.append((r+dr, c+dc, path+char))


door_keyboard = Keyboard('789', '456', '123', ' 0A')
dir_keyboard = Keyboard(' ^A', '<v>')

@cache
def solve(code, chain_length, keyboard=dir_keyboard):
    if chain_length == 0:
        return len(code)
    result = 0
    log = []
    for a, b in zip('A' + code, code):
        paths = keyboard.get_paths(a, b)
        costs = [
            solve(path, chain_length-1)
            for path in paths
        ]
        log.append(tuple(zip(paths, costs)))
        result += min(costs)
    print(f'{chain_length} keyboards away, {code!r} needs {result} presses:')
    for press, step in zip(code, log):
        def fpc(path, cost):
            return f'{path!r} ({cost} presses)'
        if len(step) == 1:
            [path_cost] = step
            print(f'- for {press!r}: {fpc(*path_cost)}')
        else:
            print(f'- for {press!r}, use the shortest of:')
            for path_cost in step:
                print(f'  - {fpc(*path_cost)}')
    return result


def get_answer(chain_length):
    total = 0
    for line in data:
        length = solve(line, chain_length+1, door_keyboard)
        num = int(line.strip('A'))
        score = length * num
        print(f'{line}: {length} * {num} = {score}')
        total += score
    return total


print('*** part 1:', get_answer(2))
print('*** part 2:', get_answer(25))
