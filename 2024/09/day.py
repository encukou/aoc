import sys
from collections import defaultdict

data = sys.stdin.read().strip()
print(data)

file = []
for i, char in enumerate(data):
    if i % 2 == 0:
        file.extend([i // 2] * int(char))
    else:
        file.extend([None] * int(char))
print(file)

def defrag(file):
    file = file.copy()
    write_pos = 0
    while file:
        block = file.pop()
        while write_pos < len(file) and file[write_pos] != None:
            write_pos += 1
        if write_pos >= len(file):
            break
        file[write_pos] = block
        if len(file) > 50:
            print(len(file))
        else:
            print(file)
    file.append(block)
    print(file)
    return file
file = defrag(file)

checksum = sum(i * (n or 0) for i, n in enumerate(file))

print('*** part 1:', checksum)


file = []
pos = 0
for i, char in enumerate(data):
    size = int(char)
    if i % 2 == 0:
        fileno = i // 2
        block = pos, size, fileno
        file.append(block)
    else:
        block = pos, size, None
        file.append(block)
    pos += size

def calc_checksum(file):
    result = 0
    for pos, size, fileno in file:
        if fileno:
            for i in range(pos, pos + size):
                result += i * fileno
    return result

def print_file(file):
    print(file)
    fpos = 0
    for pos, size, fileno in sorted(file):
        if not size:
            continue
        assert pos == fpos
        if fileno is None:
            print('.'*size, end='')
        else:
            print(f'{fileno}'*size, end='')
        fpos += size
    print(flush=True)
print_file(file)

first_space_by_size = defaultdict(int)
max_fileno = max(fileno for pos, size, fileno in file if fileno is not None)
current_pos = len(file) - 1
for moved_fileno in reversed(range(max_fileno+1)):
    print(moved_fileno, len(file), flush=True)
    while True:
        try:
            pos, size, fileno = file[current_pos]
        except IndexError:
            continue
        if fileno == moved_fileno:
            break
        current_pos -= 1
    else:
        raise ValueError()
    first_space = first_space_by_size[size]
    for sp_i, (sp_pos, sp_size, sp_fileno) in enumerate(file[first_space:], start=first_space):
        if sp_pos > pos:
            break
        if sp_fileno is None and sp_size >= size:
            new_block = sp_pos, size, fileno
            new_space_size = sp_size - size
            new_space = sp_pos + size, new_space_size, sp_fileno
            replaced_space = pos, size, sp_fileno
            file[current_pos] = replaced_space
            file[sp_i] = new_block
            first_space_by_size[size] = sp_i
            if new_space_size:
                file.append(new_space)
                file.sort()
            if len(file) < 50:
                print(file)
            break

    if len(file) < 50:
        print_file(file)


print('*** part 2:', calc_checksum(file))
