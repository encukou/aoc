import sys
import collections

data = sys.stdin.read().splitlines()
print(data)

CARDS = {c: v for v, c in enumerate(reversed('AKQJT98765432'))}

def key(hand):
    secondary = tuple(CARDS[c] for c in hand)
    tp = tuple(n for k, n in collections.Counter(hand).most_common())
    match tp:
        case [5]:
            return 6, secondary
        case [4, 1]:
            return 5, secondary
        case [3, 2]:
            return 4, secondary
        case [3, 1, 1]:
            return 3, secondary
        case [2, 2, 1]:
            return 2, secondary
        case [2, 1, 1, 1]:
            return 1, secondary
        case [1, 1, 1, 1, 1]:
            return 0, secondary
        case _:
            raise ValueError()

def fmt_score(score):
    tp, secondary = score
    return f"{str(tp)}, ({', '.join(format(n, '2d') for n in secondary)})"

lines = (l.split() for l in data)
hands = sorted((key(hand), hand, int(bid)) for hand, bid in lines)
winnings = 0
for line in enumerate(hands, start=1):
    rank, (score, hand, bid) = line
    new = rank * bid
    print(f'{rank:4}. {fmt_score(score)}: {hand} @{bid:3} -> {new}')
    winnings += new

print('*** part 1:', winnings)
# 252103402 wrong

CARDS = {c: v for v, c in enumerate(reversed('AKQT98765432J'))}

def split_jokers(hand):
    if 'J' in hand:
        jidx = hand.index('J')
        yield from (
            h
            for c in CARDS.keys() - {'J'}
            for h in split_jokers(hand[:jidx] + c + hand[jidx+1:])
        )
    else:
        yield hand

def key2(hand):
    orig_rank, orig_secondary = key(hand)
    new_rank, new_secondary = max(key(h) for h in split_jokers(hand))
    return new_rank, orig_secondary

def fmt_score(score):
    tp, secondary = score
    return f"{str(tp)}, ({', '.join(format(n, '2d') for n in secondary)})"

lines = (l.split() for l in data)
hands = sorted((key2(hand), hand, int(bid)) for hand, bid in lines)
winnings = 0
for line in enumerate(hands, start=1):
    rank, (score, hand, bid) = line
    new = rank * bid
    print(f'{rank:4}. {fmt_score(score)}: {hand} @{bid:3} -> {new}')
    winnings += new


print('*** part 2:', winnings)
# 252299873
