import sys
import collections

data = sys.stdin.read().splitlines()
print(data)


registers = collections.defaultdict(int)
sound = None
pc = 0
while True:
    instruction = data[pc]
    try:
        def get_num(n):
            try:
                return int(n)
            except ValueError:
                return registers[n]
        match instruction.split():
            case 'set', dst, num:
                num = get_num(num)
                registers[dst] = num
            case 'add', dst, num:
                num = get_num(num)
                registers[dst] += num
            case 'mul', dst, num:
                num = get_num(num)
                registers[dst] *= num
            case 'mod', dst, num:
                num = get_num(num)
                registers[dst] %= num
            case 'snd', num:
                num = get_num(num)
                sound = num
            case 'rcv', num:
                num = get_num(num)
                if num:
                    print('*** part 1:', sound)
                    break
            case 'jgz', num, offset:
                num = get_num(num)
                if num > 0:
                    pc += get_num(offset)
                    continue
            case _:
                raise ValueError(instruction)
    finally:
        print(instruction, dict(registers), sound)
    pc += 1






print('*** part 2:', ...)
