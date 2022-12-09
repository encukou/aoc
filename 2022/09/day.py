import sys

data = [d.strip().splitlines() for d in sys.stdin.read().split('---')]
print(data)

def sgn(n):
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0

head = (0, 0)
tail = (0, 0)
tail_positions = {tail}
for line in data[0]:
    print(line)
    direction, count = line.split()
    for i in range(int(count)):
        head_r, head_c = head
        match direction:
            case 'R':
                head_c +=1
            case 'L':
                head_c -=1
            case 'U':
                head_r -=1
            case 'D':
                head_r +=1
            case _:
                raise ValueError(direction)
        head = head_r, head_c
        tail_r, tail_c = tail
        if tail_r < head_r-1 and tail_c == head_c:
            tail_r += 1
        elif tail_r > head_r+1 and tail_c == head_c:
            tail_r -= 1
        elif tail_c < head_c-1 and tail_r == head_r:
            tail_c += 1
        elif tail_c > head_c+1 and tail_r == head_r:
            tail_c -= 1
        elif (
            tail_c != head_c and tail_r != head_r
            and abs(tail_c - head_c) > 1
            or abs(tail_r - head_r) > 1
        ):
            tail_r += sgn(head_r - tail_r)
            tail_c += sgn(head_c - tail_c)
        tail = tail_r, tail_c
        print(head, tail)
        tail_positions.add(tail)
print(tail_positions)

print('*** part 1:', len(tail_positions))

rope = [(0, 0)] * 10
tail_positions = set()
for line in data[-1]:
    print(line)
    direction, count = line.split()
    for i in range(int(count)):
        head_r, head_c = rope[0]
        match direction:
            case 'R':
                head_c +=1
            case 'L':
                head_c -=1
            case 'U':
                head_r -=1
            case 'D':
                head_r +=1
            case _:
                raise ValueError(direction)
        rope[0] = head_r, head_c
        for n, _ in enumerate(rope[:-1]):
            head_r, head_c = rope[n]
            tail_r, tail_c = rope[n+1]
            if tail_r < head_r-1 and tail_c == head_c:
                tail_r += 1
            elif tail_r > head_r+1 and tail_c == head_c:
                tail_r -= 1
            elif tail_c < head_c-1 and tail_r == head_r:
                tail_c += 1
            elif tail_c > head_c+1 and tail_r == head_r:
                tail_c -= 1
            elif (
                tail_c != head_c and tail_r != head_r
                and abs(tail_c - head_c) > 1
                or abs(tail_r - head_r) > 1
            ):
                tail_r += sgn(head_r - tail_r)
                tail_c += sgn(head_c - tail_c)
            rope[n+1] = tail_r, tail_c
        tail_positions.add(rope[-1])
        print(rope)
print(tail_positions)


print('*** part 2:', len(tail_positions))
