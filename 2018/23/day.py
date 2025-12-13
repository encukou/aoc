from pprint import pp
import dataclasses
import functools
import sys
import re

data = sys.stdin.read().splitlines()

RE = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)')

@dataclasses.dataclass
class Bot:
    x: int
    y: int
    z: int
    r: int

    @functools.cached_property
    def u(self): return +self.x +self.y -self.z
    @functools.cached_property
    def v(self): return +self.x -self.y +self.z
    @functools.cached_property
    def w(self): return -self.x +self.y +self.z

    def __hash__(self):
        return hash(self.key)

    def __lt__(self, other):
        return self.key < other.key

    @functools.cached_property
    def key(self):
        return self.x, self.y, self.z, self.r

    @classmethod
    def from_uvw(cls, u, v, w, r=0):
        return cls((u+v)//2, (u+w)//2, (v+w)//2, r)

    def planes(self, idx):
        n = [self.u, self.v, self.w][idx]
        yield n - self.r, 'add', self
        yield n + self.r, 'del', self

bots = []
strongest = None
for line in data:
    bot = Bot(*(int(n) for n in RE.fullmatch(line).groups()))
    bots.append(bot)
    if strongest is None or bot.r > strongest.r:
        strongest = bot

n_in_range = 0
for bot in bots:
    dist = abs(bot.x-strongest.x)+abs(bot.y-strongest.y)+abs(bot.z-strongest.z)
    if dist <= strongest.r:
        print(bot, dist, 'in range', strongest.r)
        n_in_range += 1
    else:
        print(bot, dist, 'out of range')


print('*** part 1:', n_in_range)

def get_planes(bots, index):
    result = []
    for bot in bots:
        result.extend(bot.planes(index))
    result.sort()
    return result

u_planes = get_planes(bots, 0)
pp(u_planes)

def absmin_from_range(a, b):
    if a <= 0 and b >= 0:
        return 0
    if b <= 0 and a >= 0:
        return 0
    return min(abs(a), abs(b))

def bot_planes_gen(planes, index):
    bots_now = set()
    for (c, a, bot), (nc, na, nbot) in zip(planes, planes[1:]):
        if a == 'add':
            bots_now.add(bot)
        elif a == 'del':
            bots_now.remove(bot)
        else:
            raise ValueError(a)
        if c != nc or a != na:
            yield absmin_from_range(c, nc), set(bots_now)

def bot_planes(planes, index):
    result = list(bot_planes_gen(planes, index))
    result.sort(key=lambda rb: -len(rb[-1]))
    return result

max_bots = 0
max_ranges = None
u_bots = set()
for u, u_bots in bot_planes(u_planes, 0):
    print()
    print(f'{u=} {len(u_bots)}')
    if len(u_bots) < max_bots:
        print(f'(u skip: <{max_bots})')
        continue
    v_planes = get_planes(u_bots, 1)
    pp(v_planes)
    for v, v_bots in bot_planes(v_planes, 1):
        print(f'{v=} {len(v_bots)}')
        if len(v_bots) < max_bots:
            print(f'(v skip: <{max_bots})')
            continue
        w_planes = get_planes(v_bots, 2)
        pp(w_planes)
        for w, w_bots in bot_planes(w_planes, 2):
            print(f'{w=} {len(w_bots)}')
            if len(w_bots) < max_bots:
                print(f'(w skip: <{max_bots})')
                continue
            print(u, v, w, len(w_bots))
            if len(w_bots) > max_bots:
                print(f'new max!')
                max_bots = len(w_bots)
                max_ranges = u, v, w
            else:
                if u+v+w < sum(max_ranges):
                    print(f'better max!')
                    max_bots = len(w_bots)
                    max_ranges = u, v, w

result = Bot.from_uvw(*max_ranges)
print(f'{max_ranges=}', result)

print('*** part 2:', result.u + result.v + result.w)
