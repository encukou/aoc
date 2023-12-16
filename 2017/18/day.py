import sys
import collections

data = sys.stdin.read().splitlines()
print(data)


class Program:
    def __init__(self, p=None, pipe_r=(), pipe_w=()):
        self.registers = collections.defaultdict(int)
        self.state = 'run'
        self.pc = 0
        self.sound = None
        self.pipe_r = pipe_r
        self.pipe_w = pipe_w
        if p is None:
            self.part1 = True
            self.progid = 0
        else:
            self.part1 = False
            self.progid = p
            self.registers['p'] = p
            self.num_sends = 0

    def step(self):
        pc = self.pc
        if pc < 0 or pc >= len(data):
            self.state = 'done'
            return
        instruction = data[pc]
        registers = self.registers
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
                case 'jgz', num, offset:
                    num = get_num(num)
                    if num > 0:
                        self.pc += get_num(offset)
                        return
                case 'snd', num:
                    num = get_num(num)
                    if self.part1:
                        self.sound = num
                    else:
                        self.pipe_w.append(num)
                        self.num_sends += 1
                        print(self.num_sends)
                case 'rcv', num:
                    if self.part1:
                        num = get_num(num)
                        if num:
                            self.result = self.sound
                            self.state = 'done'
                            return
                    else:
                        if self.pipe_r:
                            registers[num] = self.pipe_r.pop(0)
                            self.state = 'run'
                        else:
                            self.state = 'locked'
                            return
                case _:
                    raise ValueError(instruction)
        finally:
            print(self.progid, self.state, pc, instruction, dict(registers), self.sound, len(self.pipe_r), len(self.pipe_w))
        self.pc += 1

prog = Program()
while prog.state == 'run':
    prog.step()

print('*** part 1:', prog.sound)

pipes = [], []
progs = Program(0, pipes[0], pipes[1]), Program(1, pipes[1], pipes[0])
while True:
    for i, prog in enumerate(progs):
        prog.step()
        while prog.state == 'run':
            prog.step()
        prog.step()
    if (progs[0].state == 'locked'
        and progs[1].state == 'locked'
        and not any(pipes)
    ):
        break

print('*** part 2:', progs[1].num_sends)
