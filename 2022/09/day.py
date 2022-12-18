import sys

data = [d.strip().splitlines() for d in sys.stdin.read().split('---')]
print(data)

def abs_sgn(n):
    """Return the absolute value and sign (as -1, 1 or 0) of n

    Sign is 1 (positive), -1 (negative), or 0, see:
    https://en.wikipedia.org/wiki/Sign_function
    """
    if n > 0:
        return n, 1
    if n < 0:
        return -n, -1
    return 0, 0

def gen_positions(rope_length, instructions):
    rope = [(0, 0)] * rope_length
    tail_positions = set()
    yield rope
    for line in instructions:
        print(line)
        direction, count = line.split()
        for i in range(int(count)):
            # Move the "head" (first knot)
            # `r` means row, `c` means column
            head_r, head_c = rope[0]
            match direction:
                case 'R': head_c +=1
                case 'L': head_c -=1
                case 'D': head_r +=1
                case 'U': head_r -=1
                case _:
                    raise ValueError(direction)
            rope[0] = head_r, head_c
            # Move the rest of the rope
            for n, _ in enumerate(rope[:-1]):
                leader_r, leader_c = rope[n]
                follower_r, follower_c = rope[n+1]
                # Get distance and direction for each axis
                dist_r, dir_r = abs_sgn(leader_r - follower_r)
                dist_c, dir_c = abs_sgn(leader_c - follower_c)
                # Move "follower" knot if it's more than 2 spots away
                if max(dist_r, dist_c) >= 2:
                    follower_r += dir_r
                    follower_c += dir_c
                rope[n+1] = follower_r, follower_c
            yield rope

def solve(rope_length, instructions):
    tail_positions = set()
    for rope in gen_positions(rope_length, instructions):
        # Record the tail (last knot) position
        tail_positions.add(rope[-1])
        print(rope)
    return len(tail_positions)

if __name__ == '__main__':
    print('*** part 1:', solve(2, data[0]))
    print('*** part 2:', solve(10, data[-1]))
