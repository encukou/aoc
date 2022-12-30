import sys

data = sys.stdin.read().strip()

TRAP_PATTERNS = {
    '^^.',
    '.^^',
    '^..',
    '..^',
}

def count_safe(row, num_rows):
    num_safe = 0
    for i in range(1, num_rows+1):
        num_safe += row.count('.')
        print(f'{i:2} {row} {num_safe}')
        new_row = []
        for a, b, c in zip('.' + row, row, row[1:] + '.'):
            if a+b+c in TRAP_PATTERNS:
                new_row.append('^')
            else:
                new_row.append('.')
        row = ''.join(new_row)
    print('->', num_safe)
    return num_safe

assert count_safe('..^^.', 3) == 6
assert count_safe('.^^.^.^^^^', 10) == 38

print(f'*** part 1: {count_safe(data, 40)}')
print(f'*** part 2: {count_safe(data, 400000)}')
