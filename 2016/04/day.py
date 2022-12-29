import sys
from collections import Counter

data = sys.stdin.read().splitlines()

def parse_room_line(line):
    name, rest = line[:-1].rsplit('-', 1)
    sector, hashstr = rest.split('[')
    return name, int(sector), hashstr

def is_real(name, sector, hashstr):
    counter = Counter(name)
    del counter['-']
    pairs = sorted((-n, c) for c, n in counter.most_common())
    expected = ''.join(c for n, c in pairs[:5])
    return hashstr == expected

assert is_real(*parse_room_line('aaaaa-bbb-z-y-x-123[abxyz]'))
assert is_real(*parse_room_line('a-b-c-d-e-f-g-h-987[abcde]'))
assert is_real(*parse_room_line('not-a-real-room-404[oarel]'))
assert not is_real(*parse_room_line('totally-real-room-200[decoy]'))

def decrypt_name(encrypted_name, sector):
    result = []
    for char in encrypted_name:
        if char == '-':
            result.append(' ')
        else:
            result.append(chr((ord(char) - ord('a') + sector) % 26 + ord('a')))
    return ''.join(result)

sector_sum = 0
for line in data:
    name, sector, hashstr = parse_room_line(line)
    real = is_real(name, sector, hashstr)
    decrypted = decrypt_name(name, sector)
    print(' *'[real], decrypted, sector)
    if real:
        if 'northpole' in decrypted:
            print("That's it!")
            part2 = sector
        sector_sum += sector
        if 'elf' in name:
            exit()

print(f'*** part 1: {sector_sum}')

assert decrypt_name('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

print(f'*** part 2: {part2}')
