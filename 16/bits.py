import dataclasses
import operator
from functools import reduce

@dataclasses.dataclass
class Packet:
    version: int
    type: int
    value: int = None
    children: list = None

    def dump(self, level=0):
        if self.children is None:
            print(f'{" " * level}v{self.version} t={self.type}: {self.value}')
        else:
            print(f'{" " * level}v{self.version} t={self.type}:')
            for child in self.children:
                child.dump(level+1)

    def get_version_sum(self):
        result = self.version
        if self.children:
            for child in self.children:
                result += child.get_version_sum()
        return result

    def evaluate(self):
        if self.children is None:
            return self.value
        _eval_children = (p.evaluate() for p in self.children)
        match self.type:
            case 0:
                return sum(_eval_children)
            case 1:
                return reduce(operator.mul, _eval_children)
            case 2:
                return min(_eval_children)
            case 3:
                return max(_eval_children)
            case 4:
                return self.value
            case 5:
                return int(next(_eval_children) > next(_eval_children))
            case 6:
                return int(next(_eval_children) < next(_eval_children))
            case 7:
                return int(next(_eval_children) == next(_eval_children))
            case bad_type:
                raise ValueError(bad_type)

class Parser:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.buf = ''
        self.bits_read = 0

    def get_bits_upto(self, n):
        buf = self.buf
        if buf == '':
            buf = format(int(self.source[self.pos], 16), '04b')
            self.pos += 1
        if len(buf) <= n:
            self.buf = ''
            self.bits_read += len(buf)
            return buf
        else:
            self.buf = buf[n:]
            self.bits_read += n
            return buf[:n]

    def get_n_bits(self, n):
        bits = ''
        while len(bits) < n:
            bits += self.get_bits_upto(n - len(bits))
        return bits

    def get_packet(self):
        result = Packet(
            version=int(self.get_n_bits(3), 2),
            type=int(self.get_n_bits(3), 2),
        )
        if result.type == 4:
            value = 0
            while True:
                value *= 2**4
                chunk = self.get_n_bits(5)
                value += int(chunk[1:], 2)
                if chunk[0] == '0':
                    break
            result.value = value
        else:
            if self.get_n_bits(1) == '0':
                length = int(self.get_n_bits(15), 2)
                stop_at = self.bits_read + length
                result.children = []
                while self.bits_read < stop_at:
                    result.children.append(self.get_packet())
            else:
                num = int(self.get_n_bits(11), 2)
                result.children = []
                for i in range(num):
                    result.children.append(self.get_packet())
        return result

def parse(s):
    return Parser(s).get_packet()

print('test 2021:', parse('D2FE28'))
print('test op0:', parse('38006F45291200'))
print('test op1:', parse('EE00D40C823060'))
parse('8A004A801A8002F478').dump()
print('vs', parse('8A004A801A8002F478').get_version_sum())
parse('620080001611562C8802118E34').dump()
print('vs', parse('620080001611562C8802118E34').get_version_sum())
parse('C0015000016115A2E0802F182340').dump()
print('vs', parse('C0015000016115A2E0802F182340').get_version_sum())
parse('A0016C880162017C3686B18A3D4780').dump()
print('vs', parse('A0016C880162017C3686B18A3D4780').get_version_sum())

assert parse('C200B40A82').evaluate() == 3
assert parse('04005AC33890').evaluate() == 54
assert parse('880086C3E88112').evaluate() == 7
assert parse('CE00C43D881120').evaluate() == 9
assert parse('D8005AC2A8F0').evaluate() == 1
assert parse('F600BC2D8F').evaluate() == 0
assert parse('9C005AC2F8F0').evaluate() == 0
assert parse('9C0141080250320F1802104A08').evaluate() == 1

with open('data.txt') as file:
    packet = parse(file.read().strip())
packet.dump()
print('Part 1:', packet.get_version_sum())
print('Part 2:', packet.evaluate())
