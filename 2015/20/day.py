import sys
from heapq import heappush, heappop
import itertools
import time

maximum = int(sys.stdin.read())

next_stops = []
max_so_far = 0
for house_num in itertools.count(start=1):
    # An Elf starts here
    heappush(next_stops, (house_num, house_num))
    # Elves stop at this house
    presents = 0
    while next_stops[0][0] == house_num:
        house_num, elf = heappop(next_stops)
        presents += elf * 10
        #print(f'Elf {elf} stops at house {house_num} which now has {presents} gifts.')
        heappush(next_stops, (house_num + elf, elf))
    if presents > max_so_far:
        print(f'House {house_num:_} has {presents:_} gifts')
        max_so_far = presents
    if presents >= maximum:
        print(f'*** part 1: {house_num}')
        break

next_stops = []
max_so_far = 0
for house_num in itertools.count(start=1):
    # An Elf starts here
    heappush(next_stops, (house_num, house_num, 50))
    # Elves stop at this house
    presents = 0
    while next_stops[0][0] == house_num:
        house_num, elf, remaining = heappop(next_stops)
        presents += elf * 11
        #print(f'Elf {elf} stops at house {house_num} which now has {presents} gifts.')
        if remaining:
            heappush(next_stops, (house_num + elf, elf, remaining - 1))
    if presents > max_so_far:
        print(f'House {house_num:_} has {presents:_} gifts')
        max_so_far = presents
    if presents >= maximum:
        print(f'*** part 2: {house_num}')
        break
