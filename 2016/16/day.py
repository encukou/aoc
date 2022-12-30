import sys

data = sys.stdin.read().strip()

swap_digits = str.maketrans('01', '10')

def generate_data(string, target_length):
    while len(string) < target_length:
        old = string
        string = string + '0' + string.translate(swap_digits)[::-1]
        if len(string) < 100:
            print('gen', old, '->', string)
        else:
            print('gen', f'*{len(old)}', '->', f'*{len(string)}')
    return string[:target_length]

assert generate_data('1', 3) == '100'
assert generate_data('0', 3) == '001'
assert generate_data('11111', 11) == '11111000000'
assert generate_data('111100001010', 25) == '1111000010100101011110000'

def checksum(string):
    while len(string) % 2 == 0:
        old = string
        result = []
        for a, b in zip(string[0::2], string[1::2]):
            if a == b:
                result.append('1')
            else:
                result.append('0')
        string = ''.join(result)
        if len(old) < 100:
            print('csm', old, '->', string)
        else:
            print('csm', f'*{len(old)}', '->', f'*{len(string)}')
    return string

assert checksum('110010110100') == '100'

def solve(string, length):
    data = generate_data(string, length)
    return checksum(data)

assert solve('10000', 20) == '01100'

print(f'*** part 1: {solve(data, 272)}')
print(f'*** part 2: {solve(data, 35651584)}')
