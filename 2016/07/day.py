import sys
import re

data = sys.stdin.read().strip().splitlines()

HYPERNET_RE = re.compile(r'(?<=\[|\])')
ABBA_RE = re.compile(r'(.)(.)\2\1')

def supports_tls(address):
    result = False
    for segment in HYPERNET_RE.split(address + '['):
        if not segment:
            continue
        match = ABBA_RE.search(segment)
        matched = match and len(set(match[0])) > 1
        print(segment, matched, result)
        if segment[-1] == '[':
            if matched:
                result = True
        elif segment[-1] == ']':
            if matched:
                return False
        else:
            fail()
    return result

assert supports_tls('abba[mnop]qrst')
assert not supports_tls('abcd[bddb]xyyx')
assert not supports_tls('aaaa[qwer]tyui')
assert supports_tls('ioxxoj[asdfgh]zxcvbn')

print(f'*** part 1: {sum(bool(supports_tls(line)) for line in data)}')

XYX_RE = re.compile(r'(?=(.)(.)\1)')

def supports_ssl(address):
    result = False
    abas = set()
    babs = set()
    for segment in HYPERNET_RE.split(address + '['):
        if not segment:
            continue
        matches = [*XYX_RE.finditer(segment)]
        if segment[-1] == '[':
            abas.update(m[1]+m[2] for m in matches)
        elif segment[-1] == ']':
            babs.update(m[2]+m[1] for m in matches)
        else:
            fail()
    print(abas, babs)
    return abas & babs


assert supports_ssl('aba[bab]xyz')
assert not supports_ssl('xyx[xyx]xyx')
assert supports_ssl('aaa[kek]eke')
assert supports_ssl('zazbz[bzb]cdb')

print(f'*** part 2: {sum(bool(supports_ssl(line)) for line in data)}')
