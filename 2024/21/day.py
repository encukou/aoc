import collections
from functools import cached_property
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
                heads.append((r+dr, c+dc, path+char))

class Keypad:
    def score(self, door_code):
        number = int(door_code.strip('A'))
        total_path = ''
        for a, b in zip('A' + door_code, door_code):
            paths = list(self.get_paths(a, b))
            path = paths[0]
            self.print(paths)
            total_path += path
        total_length = len(total_path)
        score = number * total_length
        self.print(f'{door_code}: {total_length} * {number} = {score} ({total_path})')
        return score

    def wrap(self):
        return DirKeypad(self)

    def print(self, *args, **kwargs):
        print(('░ ' * self.level).strip(), *args, **kwargs)

class DoorKeypad(Keypad):
    level = 0
    keyboard = Keyboard('789', '456', '123', ' 0A')

    def get_paths(self, door_a, door_b):
        return self.keyboard.get_paths(door_a, door_b)

class DirKeypad(Keypad):
    keyboard = Keyboard(' ^A', '<v>')
    def __init__(self, next_keypad):
        self.next_keypad = next_keypad
        self.level = next_keypad.level + 1

    def get_paths(self, door_a, door_b):
        paths = list(self._get_paths(door_a, door_b))
        min_length = min(len(p) for p in paths)
        return [p for p in paths if len(p) == min_length]

    def _get_paths(self, door_a, door_b):
        if door_a == door_b:
            yield 'A'
        for next_path in self.next_keypad.get_paths(door_a, door_b):
            yield from self.get_my_paths('A' + next_path)

    def get_my_paths(self, next_path):
        if next_path == 'A':
            yield ''
            return
        self.print(f'Recursing for: {next_path}')
        nexts = list(self.get_my_paths(next_path[1:]))
        self.print(f'Finding possibilities for: {next_path}')
        for p in self.keyboard.get_paths(next_path[0], next_path[1]):
            for nxt in nexts:
                self.print(f'possibility for {next_path}: {p}{nxt}')
                yield p + nxt

keypad = DoorKeypad()
keypad = keypad.wrap()
keypad = keypad.wrap()
total = 0
for line in data:
    total += keypad.score(line)

print('*** part 1:', total)




print('*** part 2:', ...)
