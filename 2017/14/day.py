import sys

data = sys.stdin.read().strip()
print(data)

def do_round(string, lengths, current_position=0, skip_size=0):
    string = list(string)
    for length in lengths:
        length = int(length)
        string = string[current_position:] + string[:current_position]
        string[:length] = reversed(string[:length])
        string = string[-current_position:] + string[:-current_position]
        current_position += length + skip_size
        current_position %= len(string)
        skip_size += 1
    return string, current_position, skip_size
def knothash(data):
    lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    string = list(range(256))
    current_position = skip_size = 0
    for i in range(64):
        string, current_position, skip_size = do_round(
            string, lengths, current_position, skip_size,
        )
    dense_hash = []
    for start in range(16):
        nums = string[start*16 : start*16+16]
        value = 0
        for n in nums:
            value ^= n
        dense_hash.append(value)
    knot = ''.join(f'{n:02x}' for n in dense_hash)
    return knot

used_coords = set()
for i in range(128):
    khash = int(knothash(f'{data}-{i}'), 16)
    bits = f'{khash:0128b}'
    used_coords.update(((i, n) for n, b in enumerate(bits) if b == '1'))
    print(bits.replace('0', '.').replace('1', '#'))

print('*** part 1:', len(used_coords))


num_regions = 0
while used_coords:
    num_regions += 1
    to_remove = {used_coords.pop()}
    while to_remove:
        r, c = to_remove.pop()
        for dr, dc in (+1, 0), (0, -1), (0, +1), (-1, 0):
            neighbor = r+dr, c+dc
            if neighbor in used_coords:
                to_remove.add(neighbor)
                used_coords.discard(neighbor)


print('*** part 2:', num_regions)
