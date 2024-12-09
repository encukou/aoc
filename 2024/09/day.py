import sys

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
defrag(file)

checksum = sum(i * n for i, n in enumerate(file))

print('*** part 1:', checksum)




print('*** part 2:', ...)
