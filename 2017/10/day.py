import sys

data = sys.stdin.read().strip()
print(data)

if ', ' in data:
    string = list(range(5))
else:
    string = list(range(256))

def do_round(string, lengths, current_position=0, skip_size=0):
    string = list(string)
    for length in lengths:
        length = int(length)
        print(length)
        string = string[current_position:] + string[:current_position]
        string[:length] = reversed(string[:length])
        string = string[-current_position:] + string[:-current_position]
        current_position += length + skip_size
        current_position %= len(string)
        skip_size += 1
        print('+++', length, string, current_position, skip_size)
    return string, current_position, skip_size

string_part1, *_ = do_round(string, data.replace(',', ' ').split())
print('*** part 1:', string_part1[0] * string_part1[1])

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
        print('nums', nums)
        value = 0
        for n in nums:
            value ^= n
        dense_hash.append(value)
    print(f'{dense_hash=}')
    knot = ''.join(f'{n:02x}' for n in dense_hash)
    print(f'{knot=}')
    return knot


assert knothash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert knothash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert knothash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert knothash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'


print('*** part 2:', knothash(data))
