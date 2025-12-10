import dataclasses
import functools
import sys
import re

data = sys.stdin.read().splitlines()
print(data)

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

    @classmethod
    def from_uvw(cls, u, v, w):
        return cls((u+v)//2, (u+w)//2, (v+w)//2)

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




print('*** part 2:', ...)
