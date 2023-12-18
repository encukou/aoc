import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    'R': (0, +1),
    'D': (+1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}
CHARS = {
    'R': '#-#',
    'D': ".|'",
    'L': "#-#",
    'U': "'|.",
}

def draw_and_count(dug):
    total = 0
    rs = [r for r, c in dug]
    cs = [c for r, c in dug]
    for r in range(min(rs), max(rs)+1):
        is_in = False
        print(f'{r:3}. ', end='')
        for c in range(min(cs), max(cs)+1):
            char = dug.get((r, c))
            if char:
                print(char, end='')
                if char in {'.', '|'}:
                    is_in = not is_in
                total += 1
            elif is_in:
                print('#', end='')
                total += 1
            else:
                print(' ', end='')
        print()
    return total

r = 0
c = 0
dug = {}
for line in data:
    direction, distance, color = line.split()
    distance = int(distance)
    assert distance > 0
    dr, dc = DIRS[direction]
    chars = CHARS[direction]
    def record(char):
        if (r, c) not in dug or char != '#':
            dug[r, c] = char
    record(chars[0])
    for i in range(distance - 1):
        r += dr
        c += dc
        record(chars[1])
    r += dr
    c += dc
    record(chars[2])
    if len(data) < 20:
        print(dug)
        draw_and_count(dug)

print(dug)

print('*** part 1:', draw_and_count(dug))

def range_key(r):
    return r.start, r.stop

def merge_ranges(ranges):
    if not ranges:
        return []
    ranges = sorted(ranges, key=range_key)
    result = []
    current = ranges.pop(0)
    for next in ranges:
        if next.start <= current.stop:
            current = range(current.start, max(next.stop, current.stop))
        else:
            result.append(current)
            current = next
    result.append(current)
    return result

DIR_CODES = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}
marks = {}
r = 0
c = 0
for line in data:
    direction, distance, color = line.split()
    assert color[:2] == '(#'
    distance = int(color[2:-2], 16)
    direction = DIR_CODES[color[-2]]
    assert color[-1] == ')'
    print(direction, distance)
    dr, dc = DIRS[direction]
    nr = r + dr * distance
    nc = c + dc * distance
    def put_mark(r, c, mark):
        mark_row = marks.setdefault(r, {})
        assert c not in mark_row
        mark_row[c] = mark
    if direction == 'U':
        put_mark(r, c, "'")
        put_mark(nr, c, ".")
    elif direction == 'D':
        put_mark(r, c, ".")
        put_mark(nr, c, "'")
    r = nr
    c = nc
print(marks)
current_marks = set()
current_ranges = []
total = 0
prev_r = 0
for r, mark_row in sorted(marks.items()):
    new = sum(len(r) for r in current_ranges) * (r - prev_r - 1)
    total += new
    print(r, new, '->', total)
    for c, mark in mark_row.items():
        if mark == '.':
            assert c not in current_marks
            current_marks.add(c)
        else:
            assert c in current_marks
            current_marks.remove(c)
    assert len(current_marks) % 2 == 0
    mark_row = sorted(mark_row.items())
    current_marks_sorted = sorted(current_marks)
    new_ranges = [range(a, b+1) for a, b in zip(
        current_marks_sorted[0::2],
        current_marks_sorted[1::2],
    )]
    line_ranges = merge_ranges(current_ranges + new_ranges)
    new = sum(len(r) for r in line_ranges)
    total += new
    current_ranges = new_ranges
    print(r, mark_row, current_ranges, new, '->', total)
    prev_r = r


print('*** part 2:', total)
