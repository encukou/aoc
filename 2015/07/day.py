import sys
import numpy

data = sys.stdin.read().strip().splitlines()

example = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
*ALL* -> a
""".strip().splitlines()

MASK = 0xffff

def solve(lines, override=()):
    instructions = dict(reversed(line.split(' -> ')) for line in lines)
    instructions.update(override)
    def solve_one(name):
        try:
            instruction = instructions[name]
        except KeyError:
            return int(name)
        if isinstance(instruction, int):
            return instruction
        match instruction.split():
            case ['*ALL*']:
                result = {n: solve_one(n) for n in sorted(instructions) if n != name}
            case [s]:
                try:
                    result = int(s)
                except ValueError:
                    result = solve_one(s)
            case left, 'AND', right:
                result = (solve_one(left) & solve_one(right)) & MASK
            case left, 'OR', right:
                result = (solve_one(left) | solve_one(right)) & MASK
            case left, 'LSHIFT', right:
                result = (solve_one(left) << solve_one(right)) & MASK
            case left, 'RSHIFT', right:
                result = (solve_one(left) >> solve_one(right)) & MASK
            case 'NOT', arg:
                result = (~solve_one(arg)) & MASK
            case _:
                raise ValueError(instruction)
        instructions[name] = result
        return result
    return solve_one('a')


print(solve(example))
value_a = solve(data)
print(f'*** part 1: {value_a}')
print(f'*** part 2: {solve(data, override={"b": value_a})}')
