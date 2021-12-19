import itertools
from dataclasses import dataclass
from pprint import pprint

MATCH_COUNT = 12//2

permutations = list(itertools.product(
    itertools.permutations([0, 1, 2]),
    itertools.product([1, -1], repeat=3)
))

def permute(xyz, permutation):
    axes, dirs = permutation
    x = xyz[axes[0]] * dirs[0]
    y = xyz[axes[1]] * dirs[1]
    z = xyz[axes[2]] * dirs[2]
    return x, y, z

def permute_add(xyz, permutation, offset):
    x, y, z = permute(xyz, permutation)
    x += offset[0]
    y += offset[1]
    z += offset[2]
    return x, y, z

scanner_id = -1
unknown_scanners = {}
with open('data.txt') as f:
    for line in f:
        line = line.strip()
        print(line)
        if not line:
            continue
        if line.startswith('---'):
            scanner_id += 1
            unknown_scanners[scanner_id] = []
        else:
            x, y, z = line.split(',')
            unknown_scanners[scanner_id].append((int(x), int(y), int(z)))

known_beacons = {xyz: {0} for xyz in unknown_scanners.pop(0)}
known_scanner_ids = {0: (permutations[0], (0, 0, 0))}

pprint(permutations)
pprint(known_beacons)
pprint(unknown_scanners)

def try_match(unknown_beacons, permutation, offset):
    print(unknown_beacons, permutation, offset)
    for known_beacon in known_beacons:
        for permutation in permutations:
            for unknown_beacon in unknown_beacons:
                _perm = permute(unknown_beacon, permutation)
                offset = tuple(
                    k-u for k, u
                    in zip(known_beacon, _perm)
                )
                assert permute_add(unknown_beacon, permutation, offset) == known_beacon
                del unknown_beacon
                matched = dict.fromkeys(known_scanner_ids, 0)
                for unknown in unknown_beacons:
                    adjusted = permute_add(unknown, permutation, offset)
                    #print(f'{unknown} ¤ {permutation}/{offset} -> {adjusted}')
                    if scanner_ids := known_beacons.get(adjusted):
                        for scanner_id in scanner_ids:
                            matched.setdefault(scanner_id, 0)
                            matched[scanner_id] += 1
                            if matched[scanner_id] >= MATCH_COUNT:
                                return permutation, offset
                #pprint(matched)
    return None, None

while unknown_scanners:
    pprint(known_beacons)
    pprint(unknown_scanners)
    for unknown_id, unknown_scanner in unknown_scanners.items():
        for known_id, (permutation, offset) in known_scanner_ids.items():
            permutation, offset = try_match(
                unknown_scanner, permutation, offset,
            )
            if permutation:
                break
        else:
            continue
        break
    else:
        raise Exception('could not match anything')
    discovered_beacons = unknown_scanners.pop(unknown_id)
    print(f'Adding scanner {unknown_id}!')
    for discovered_beacon in discovered_beacons:
        adjusted = permute_add(discovered_beacon, permutation, offset)
        known_beacons.setdefault(adjusted, set()).add(unknown_id)

    pprint(sorted(known_beacons.items()))

print('Part 1:', len(known_beacons))
