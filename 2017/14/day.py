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

total = 0
for i in range(128):
    khash = int(knothash(f'{data}-{i}'), 16)
    bits = f'{khash:0128b}'
    print(bits)
    total += khash.bit_count()

print('*** part 1:', total)




print('*** part 2:', ...)
