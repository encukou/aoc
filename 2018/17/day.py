import functools
import heapq
import enum
import sys
import re

data = sys.stdin.read().splitlines()
print(data)

class State(enum.Enum):
    CLAY = '█'
    SAND = ' '
    FLOW = '|'
    STILL = '≈'
    STILL_L = '<'
    STILL_R = '>'
    DRAIN = '!'
    UNKNOWN = '*'

ground = {}

for line in data:
    comm, start, end = (
        int(n) for n
        in re.fullmatch(r'.=(\d+), .=(\d+)..(\d+)', line).groups()
    )
    if line.startswith('x'):
        for r in range(start, end+1):
            ground[r, comm] = State.CLAY
    else:
        for c in range(start, end+1):
            ground[comm, c] = State.CLAY

max_r = max(r for r, c in ground)
min_r = min(r for r, c in ground)

SPRING = 0, 500
unsettled = []
ground[SPRING] = State.FLOW
wet = set()

def push(prio, key):
    r, c = key
    heapq.heappush(unsettled, (-prio, key))
    ground[key] = State.FLOW
    if min_r <= r <= max_r:
        wet.add(key)

def pop():
    prio, key = heapq.heappop(unsettled)
    ground[key] = State.UNKNOWN
    return -prio, key

push(0, SPRING)

def state_at(key):
    return ground.get(key, State.SAND)

def symbol_at(key):
    r, c = key
    if r > max_r:
        return '!'
    return state_at(key).value

def is_passable(key):
    return ground.get(key) is None

def draw_map():
    min_r = min(r for r, c in ground)
    min_c = min(c for r, c in ground)-1
    max_r = max(r for r, c in ground)+1
    max_c = max(c for r, c in ground)+1
    for r in range(min(min_r, 0), max_r+1):
        n_wet = 0
        print(end=f'{r:4} ')
        for c in range(min_c, max_c+1):
            key = r, c
            if key in wet:
                print(end='\x1b[46m')
                n_wet += 1
            print(end=symbol_at(key))
            print(end='\x1b[m')
        print(n_wet)

def settle(key):
    ground[key] = state.STILL

i = 0
while unsettled:
    i += 1
    prio, here = pop()
    r, c = here
    below = r + 1, c
    left = r, c - 1
    right = r, c + 1
    symbols = symbol_at(left) + symbol_at(below) + symbol_at(right)
    if max_r < 100 or i < 100 or i % 100 == 0:
        print(f'{i}, uns={len(unsettled)} wet={len(wet)} {symbols}', flush=True)
        if max_r < 100 or i % 100_000 == 0:
            draw_map()
    def retry(here):
        push(prio, here)
    def consider(key):
        r, c = key
        push(prio+1, key)
    def become(symbol):
        assert ground[here] != State.CLAY
        ground[here] = State(symbol)
    match symbols:
        case '   ': retry(here), consider(below)
        case '  █': retry(here), consider(below)
        case ' ██': become('<'), consider(left)
        case ' █<': become('<'), consider(left)
        case '██<': become('≈'), consider(right)
        case '≈█<': become('≈'), consider(right)
        case '≈██': become('≈')
        case ' ≈█': become('<'), consider(left)
        case ' ≈<': become('<'), consider(left)
        case '█≈<': become('≈'), consider(right)
        case '≈≈<': become('≈'), consider(right)
        case '≈≈█': become('≈')
        case ' ≈ ': retry(here), consider(left), consider(right)
        case '█≈|': become('>')
        case '>≈|': become('>')
        case '>█ ': become('>'), consider(right)
        case '>  ': retry(here), consider(below)
        case '█  ': retry(here), consider(below)
        case ' █ ': retry(here), consider(left), consider(right)
        case ' █|': retry(here), consider(left)
        case '██|': become('>')
        case '>█|': become('>')
        case '>██': become('≈'), consider(left)
        case '>█≈': become('≈'), consider(left)
        case '██≈': become('≈')
        case ' ≈|': retry(here), consider(left)
        case '>≈█': become('≈'), consider(left)
        case '>≈≈': become('≈'), consider(left)
        case '█≈≈': become('≈')
        case '  |': retry(here), consider(below)
        case ' !█': become('!')
        case ' !|': become('!')
        case '!█|': become('<')
        case '<≈|': become('<')
        case '<≈ ': retry(here), consider(right)
        case '<█ ': retry(here), consider(right)
        case '|█ ': retry(here), consider(right)
        case '|  ': retry(here), consider(below)
        case '|██': become('<')
        case '>█<': become('≈'), consider(left), consider(right)
        case '>≈<': become('≈'), consider(left), consider(right)
        case '|≈█': become('<')
        case '|≈ ': retry(here), consider(right)
        case '█! ': become('!')
        case '|! ': become('!')
        case '|█!': become('>')
        case '|≈>': become('>')
        case '<≈>': become('!')
        case ' ! ': become('!')
        case '>≈>': become('!')
        case '|█<': become('<')
        case '|≈<': become('<')
        case '██ ': retry(here), consider(right)
        case '█≈ ': retry(here), consider(right)
        case '█ █': retry(here), consider(below)
        case '███': become('≈')
        case '█≈█': become('≈')
        case '<≈<': become('<')
        case ' < ': become('!')
        case ' > ': become('!')
        case _:
            draw_map()
            raise ValueError(repr(symbol_at(left) + symbol_at(below) + symbol_at(right)))

    continue
    if is_passable(below):
        if r < max_r:
            push(prio, here)
            push(prio+1, below)
        else:
            ground[here] = State.DRAIN
    elif state_at(below) in {State.CLAY, State.STILL}:
        if is_passable(left) or is_passable(right):
            push(prio, here)
            if is_passable(left):
                push(prio+1, left)
            if is_passable(right):
                push(prio+1, right)
        elif State.DRAIN in {state_at(left), state_at(right)}:
            ground[here] = State.DRAIN
            if state_at(left) in {State.STILL_L, State.STILL_R}:
                push(prio+1, left)
            if state_at(right) in {State.STILL_L, State.STILL_R}:
                push(prio+1, right)
        else:
            block_left = state_at(left) in {State.CLAY, State.STILL, State.STILL_L}
            block_right = state_at(right) in {State.CLAY, State.STILL, State.STILL_R}
            if block_left and block_right:
                ground[here] = State.STILL
                if state_at(left) in {State.STILL_L}:
                    push(prio+1, left)
                if state_at(right) in {State.STILL_R}:
                    push(prio+1, right)
            elif block_left:
                ground[here] = State.STILL_L
            elif block_right:
                ground[here] = State.STILL_R
            else:
                draw_map()
                raise ValueError(repr(symbol_at(left) + symbol_at(below) + symbol_at(right)))
    elif state_at(below) in {State.DRAIN}:
        ground[here] = State.DRAIN
        if state_at(left) in {State.STILL_L, State.STILL_R}:
            push(prio+1, left)
        if state_at(right) in {State.STILL_L, State.STILL_R}:
            push(prio+1, right)
    else:
        draw_map()
        raise ValueError(repr(symbol_at(left) + symbol_at(below) + symbol_at(right)))

wet -= {SPRING}
draw_map()

print('*** part 1:', len(wet))

print('*** part 2:', list(ground.values()).count(State.STILL))
