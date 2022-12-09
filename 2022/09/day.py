import sys

data = sys.stdin.read().splitlines()

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
for line in data:
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




print('*** part 2:', ...)
