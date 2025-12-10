from pprint import pp
import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0
for line in data:
    lights_in, *buttons_in, joltage_in = line.split()
    lights = sum(1<<i if (c == '#') else 0 for i, c in enumerate(lights_in[1:-1]))
    buttons = []
    for b in buttons_in:
        buttons.append(sum(1<<int(n) for n in b[1:-1].split(',')))
    joltage = [int(n) for n in joltage_in[1:-1].split(',')]
    pp((bin(lights), [bin(b) for b in buttons], joltage))

    nums = list(range(2**len(buttons)))
    nums.sort(key=int.bit_count)
    for i, num in enumerate(nums):
        print(i, num, bin(num))
        lights_now = 0
        bit = 0
        bits = num
        while bits:
            if bits % 2:
                lights_now ^= buttons[bit]
            bit += 1
            bits //= 2
        if lights_now == lights:
            print(num.bit_count())
            total += num.bit_count()
            break


print('*** part 1:', total)




print('*** part 2:', ...)
