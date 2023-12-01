import sys

data = sys.stdin.read().strip()
print(data)

if ', ' in data:
    string = list(range(5))
else:
    string = list(range(256))

current_position = 0
skip_size = 0
for length in data.replace(',', ' ').split():
    length = int(length)
    print(length)
    print('get', length, string, current_position, skip_size)
    string = string[current_position:] + string[:current_position]
    print('-->', length, string, current_position, skip_size)
    string[:length] = reversed(string[:length])
    print('rot', length, string, current_position, skip_size)
    string = string[-current_position:] + string[:-current_position]
    print('<--', length, string, current_position, skip_size)
    current_position += length + skip_size
    current_position %= len(string)
    skip_size += 1
    print('+++', length, string, current_position, skip_size)


print('*** part 1:', string[0] * string[1])




print('*** part 2:', ...)
