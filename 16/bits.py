import dataclasses

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

with open('data.txt') as file:
    packet = parse(file.read().strip())
packet.dump()
print('Part 1:', packet.get_version_sum())


