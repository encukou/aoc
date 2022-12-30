import sys
import hashlib
from collections import deque

data = sys.stdin.read().strip()

DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

OPEN = 'bcdef'
ROOM_SIZE = 4

def solve(code, find_len_longest=False):
    orig_code = code
    to_visit = deque([(code, 0, 0)])
    longest = None
    while to_visit:
        code, x, y = to_visit.popleft()
        if len(code) < 20:
            print(x, y, code)
        if x == y == ROOM_SIZE - 1:
            longest = code[len(orig_code):]
            print(orig_code, longest if len(longest) < 20 else f'*{len(longest)}')
            if not find_len_longest:
                return longest
            continue
        for (dirchar, (dx, dy)), hashchar in zip(
            DIRECTIONS.items(),
            hashlib.md5(code.encode('ascii')).hexdigest(),
        ):
            if hashchar in OPEN:
                newx = x + dx
                newy = y + dy
                if 0 <= newx < ROOM_SIZE and 0 <= newy < ROOM_SIZE:
                    newcode = code + dirchar
                    to_visit.append((newcode, newx, newy))
    print('Locked out!')
    if find_len_longest:
        return len(longest)

assert solve('hijkl') == None
assert solve('ihgpwlah') == 'DDRRRD'
assert solve('kglvqrro') == 'DDUDRLRRUDRD'
assert solve('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

print(f'*** part 1: {solve(data)}')


assert solve('ihgpwlah', find_len_longest=True) == 370
assert solve('kglvqrro', find_len_longest=True) == 492
assert solve('ulqzkmiv', find_len_longest=True) == 830

print(f'*** part 2: {solve(data, find_len_longest=True)}')
