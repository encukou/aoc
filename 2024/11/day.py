import sys

data = sys.stdin.read().split()
print(data)

stones = [int(n) for n in data]
for i in range(25):
    new_stones = []
    for stone in stones:
        s = str(stone)
        if stone == 0:
            new_stones.append(1)
        elif len(s) % 2 == 0:
            new_stones.append(int(s[len(s) // 2:]))
            new_stones.append(int(s[:len(s) // 2]))
        else:
            new_stones.append(stone * 2024)
    stones = new_stones
    print(len(stones), stones)

print('*** part 1:', len(stones))




print('*** part 2:', ...)
