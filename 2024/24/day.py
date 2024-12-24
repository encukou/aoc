import re
import sys

wire_data, gate_data = sys.stdin.read().split('\n\n')
wire_data = wire_data.splitlines()
gate_data = gate_data.splitlines()
print(wire_data, gate_data)


wires = {}
for line in wire_data:
    name, number = line.split(':')
    wires[name] = int(number)
print(wires)

unassigned_wires = set()
gates = []
for line in gate_data:
    match = re.fullmatch(r'(\w+) (\w+) (\w+) -> (\w+)', line)
    gates.append((match[1], match[3], match[2], match[4]))
    for wire in match[1], match[3], match[4]:
        if wire not in wires:
            unassigned_wires.add(wire)
print(gates)
print(unassigned_wires)

go_on = True
while go_on:
    go_on = False
    for gate in gates:
        in1, in2, op, out = gate
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




print('*** part 2:', ...)
