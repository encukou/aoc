import re
import sys

wire_data, gate_data = sys.stdin.read().split('\n\n')
wire_data = wire_data.splitlines()
gate_data = gate_data.splitlines()
print(wire_data, gate_data)


def load_wires():
    wires = {}
    for line in wire_data:
        name, number = line.split(':')
        wires[name] = int(number)
    print(wires)
    return wires
wires = load_wires()

unassigned_wires = set()
gates = {}
for line in gate_data:
    match = re.fullmatch(r'(\w+) (\w+) (\w+) -> (\w+)', line)
    gates[match[4]] = match[1], match[3], match[2]
    for wire in match[1], match[3], match[4]:
        if wire not in wires:
            unassigned_wires.add(wire)
print(gates)
print(unassigned_wires)

go_on = True
while go_on:
    go_on = False
    for out, (in1, in2, op) in gates.items():
        if in1 in wires and in2 in wires and out not in wires:
            if op == 'AND':
                wires[out] = wires[in1] & wires[in2]
            elif op == 'OR':
                wires[out] = wires[in1] | wires[in2]
            elif op == 'XOR':
                wires[out] = wires[in1] ^ wires[in2]
            else:
                raise ValueError(op)
            go_on = True
        unassigned_wires.discard(out)
    print(sorted(unassigned_wires))
print(wires)

answer = 0
for wire, val in sorted(wires.items(), reverse=True):
    if wire.startswith('z'):
        answer *= 2
        answer += val
    print(wire, val, bin(answer))


print('*** part 1:', answer)
if len(wire_data) <= 10:
    exit()

swapped_wires = set()
def swap(a, b):
    gates[a], gates[b] = gates[b], gates[a]
    swapped_wires.add(a)
    swapped_wires.add(b)

# Found semi-automatically using debug output below. (Remove to recreate).
swap('z09', 'hnd')
swap('z16', 'tdv')
swap('z23', 'bks')
swap('tjp', 'nrn')


r'''
Full adder:

carry(n-1) -----------------------+-- |[  \
                                  |   |[ ^ > -- output -->
x_n ---+- |[  \                ,--|-- |[  /
       |  |[ ^ > --- bit-sum --+  |
y-n -+-|- |[  /                |  '-- [  \
     | |                       |      [ & ) -- intermediate --- [ \
     | '-- [  \                '----- [  /                      [ |> - carry ->
     |     [ & ) --- bit-mul ---------------------------------- [ /
     '---- [  /

Bit-Sum(n) is XOR:
    - x_n
    - y_n

Bit-Mul(n) is AND:
    - x_n
    - y_n

Output is XOR:
    - Bit-Sum(n)
    - Carry(n)

Intermediate(n) is AND:
    - Bit-Sum(n)
    - Carry(n)

Carry(n+1) is OR:
    - Intermediate(n)
    - Bit-Mul(n)
'''

wires = load_wires()
functions = {w: (int(w[1:]), w[0]) for w in wires}
go_on = True
while go_on:
    go_on = False
    for out, (in1, in2, op) in gates.items():
        if out in functions:
            continue

        try:
            function1 = functions[in1]
            function2 = functions[in2]
        except KeyError:
            continue
        print(function1, function2, functions)
        function1, function2 = sorted((function1, function2))
        level1, f1 = function1
        level2, f2 = function2
        if level1 == level2:
            if f1 == 'x' and f2 == 'y' and op == 'XOR':
                functions[out] = level1, 'bit-sum'
                if level1 == 0:
                    functions[out] = level1, 'output'
            if f1 == 'x' and f2 == 'y' and op == 'AND':
                functions[out] = level1, 'bit-mul'

            if f1 == 'bit-mul' and f2 == 'intermediate' and op == 'OR':
                functions[out] = level1+1, 'carry'

            if f1 == 'bit-sum' and f2 == 'carry' and op == 'XOR':
                functions[out] = level1, 'output'

            if f1 == 'bit-sum' and f2 == 'carry' and op == 'AND':
                functions[out] = level1, 'intermediate'

        if level1 + 1 == level2:

            if level1 == 0 and f1 == 'bit-mul' and f2 == 'bit-sum' and op == 'XOR':
                # bit-sum is like carry
                functions[out] = level2, 'output'

            if level1 == 0 and f1 == 'bit-mul' and f2 == 'bit-sum' and op == 'AND':
                # bit-sum is like carry
                functions[out] = level2, 'intermediate'


        if out in functions:
            go_on = True

print(functions)
def dump(out, indent=0):
    if name := functions.get(out):
        print(' ' * indent, out, name)
    elif out in gates:
        in1, in2, op = gates[out]
        print(' ' * indent, out, '=', op)
        for input in sorted([in1, in2]):
            dump(input, indent+1)
    else:
        print(' ' * indent, out, '=', wires[out])

for wire in sorted(gates):
    if wire.startswith('z'):
        i = int(wire[1:])
        print(wire)
        dump(wire)
        if functions.get(wire) != (i, 'output'):
            for k, v in functions.items():
                if v == (i, 'output'):
                    print(f'please swap {wire} <=> {k}')

print('*** part 2:', ','.join(sorted(swapped_wires)))
