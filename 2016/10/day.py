import sys
from collections import defaultdict

data = sys.stdin.read().strip().splitlines()

bot_sources = defaultdict(set)
out_sources = {}
for line in data:
    print(line)
    match line.split():
        case 'value', val, 'goes', 'to', 'bot', bot:
            bot_sources[int(bot)].add(('v', int(val)))
        case (
            'bot', src, 'gives', 'low', 'to', low_type, low_n,
            'and', 'high', 'to', hi_type, hi_n
        ):
            for t, n, lh in (low_type, low_n, 'l'), (hi_type, hi_n, 'h'):
                key = lh, int(src)
                if t == 'bot':
                    bot_sources[int(n)].add(key)
                elif t == 'output':
                    out_sources[int(n)] = key
                else:
                    raise ValueError(t)
        case _:
            raise ValueError(line)

def resolve_source(src):
    match src:
        case 'v', num:
            return num
        case 'l', num:
            lo, hi = resolve_bot_sources(num)
            return lo
        case 'h', num:
            lo, hi = resolve_bot_sources(num)
            return hi
        case int():
            return src
        case _:
            raise ValueError(src)

def resolve_bot_sources(bot_num):
    resolved = []
    for src in bot_sources[bot_num]:
        resolved.append(resolve_source(src))
    resolved = tuple(sorted(resolved))
    print(f'Bot {bot_num} gets {resolved}')
    bot_sources[bot_num] = resolved
    if resolved == (17, 61):
        global part1_answer
        part1_answer = bot_num
    return resolved

for bot_num in sorted(bot_sources):
    resolve_bot_sources(bot_num)

print(f'*** part 1: {part1_answer}')

a, b, c = (resolve_source(out_sources[n]) for n in range(3))
print(f'*** part 2: {a*b*c}')
