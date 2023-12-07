import sys
import collections

data = sys.stdin.read().splitlines()
print(data)

CARD_SCORES = {card: val for val, card in enumerate(reversed('AKQJT98765432'))}

def score_counts(counts):
    counts = sorted(counts, reverse=True)
    match counts:
        case [5]:
            return 6
        case [4, 1]:
            return 5
        case [3, 2]:
            return 4
        case [3, 1, 1]:
            return 3
        case [2, 2, 1]:
            return 2
        case [2, 1, 1, 1]:
            return 1
        case [1, 1, 1, 1, 1]:
            return 0
        case _:
            raise ValueError(counts)

def key(hand):
    counts = collections.Counter(hand).values()
    return score_counts(counts), tuple(CARD_SCORES[c] for c in hand)

def fmt_score(score):
    tp, secondary = score
    return f"{str(tp)},({', '.join(format(n, '2d') for n in secondary)})"

def solve(key):
    lines = (l.split() for l in data)
    hands = sorted((key(hand), hand, int(bid)) for hand, bid in lines)
    winnings = 0
    for rank, (score, hand, bid) in enumerate(hands, start=1):
        winning = rank * bid
        print(f'{rank:4}. {fmt_score(score)}: {hand} @{bid:3} -> {winning}')
        winnings += winning
    return winnings

print('*** part 1:', solve(key))

WILD_CARD_SCORES = CARD_SCORES | {'J': -1}

def wild_key(hand):
    counter = collections.Counter(hand)
    n_jokers = counter.pop('J', 0)
    if counter:
        best, best_val = counter.most_common(1)[0]
    else:
        best = 'A'
    counter[best] += n_jokers
    return score_counts(counter.values()), tuple(WILD_CARD_SCORES[c] for c in hand)

print('*** part 2:', solve(wild_key))
