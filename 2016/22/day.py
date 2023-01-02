import sys
from dataclasses import dataclass
import re

data = sys.stdin.read().strip().splitlines()

LINE_RE = re.compile(r'/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%')

@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int
    #percent: int

def is_viable(src, dst):
    return src.used and src is not dst and src.used <= dst.avail

nodes = []
for i, line in enumerate(data):
    match = LINE_RE.fullmatch(line)
    if not match:
        assert i < 2
        continue
    nodes.append(Node(
        x=int(match[1]),
        y=int(match[2]),
        size=int(match[3]),
        used=int(match[4]),
        avail=int(match[5]),
        #percent=int(match[6]),
    ))
num_viable = 0
for a in nodes:
    for b in nodes:
        if is_viable(a, b):
            num_viable += 1

print(f'*** part 1: {num_viable}')

nodes_by_pos = {(n.x, n.y): n for n in nodes}
xs = {n.x for n in nodes}
ys = {n.y for n in nodes}
goal_node = nodes_by_pos[max(xs), 0]
dest_node = nodes_by_pos[0, 0]

[freenode] = [n for n in nodes if n.used == 0]
turns = 0
def draw():
    print(f'Turn {turns}')
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            node = nodes_by_pos[x, y]
            if node is goal_node:
                print('G!', end=' ')
            elif node is freenode:
                print('__', end=' ')
            elif node is dest_node:
                print('()', end=' ')
            elif node.used > freenode.avail:
                print('##', end=' ')
            else:
                print(f'::', end=' ')
        print()

def move_freenode(dx, dy):
    global freenode
    global goal_node
    global turns
    try:
        src = nodes_by_pos[freenode.x + dx, freenode.y + dy]
    except KeyError:
        return False
    if is_viable(src, freenode):
        freenode.used = src.used
        freenode.avail = freenode.size - freenode.used
        src.used = 0
        src.avail = src.size
        if src is goal_node:
            goal_node = freenode
        freenode = src
        turns += 1
        return True
    return False

while move_freenode(0, -1):
    draw()
while not move_freenode(0, -1):
    move_freenode(-1, 0)
    draw()
draw()
while move_freenode(0, -1):
    draw()
while move_freenode(1, 0):
    draw()
while goal_node != dest_node:
    for dx, dy in (0, 1), (-1, 0), (-1, 0), (0, -1), (1, 0):
        move_freenode(dx, dy)
        draw()

print(f'*** part 1: {turns}')
# 222 too high
