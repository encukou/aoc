
maze = {}

for line in """
start-co
ip-WE
end-WE
le-ls
wt-zi
end-sz
wt-RI
wt-sz
zi-start
wt-ip
YT-sz
RI-start
le-end
ip-sz
WE-sz
le-WE
le-wt
zi-ip
RI-zi
co-zi
co-le
WB-zi
wt-WE
co-RI
RI-ip
""".strip().splitlines():
    a, b = line.strip().split('-')
    maze.setdefault(a, []).append(b)
    maze.setdefault(b, []).append(a)


def num_paths(path_so_far, current_cave, can_revisit_small=False):
    if current_cave == 'end':
        return 1
    count = 0
    for next_cave in maze[current_cave]:
        if next_cave not in path_so_far or next_cave.isupper():
            count += num_paths(
                path_so_far | {current_cave},
                next_cave,
                can_revisit_small=can_revisit_small,
            )
        elif can_revisit_small and next_cave != 'start':
            count += num_paths(
                path_so_far | {current_cave},
                next_cave,
                can_revisit_small=False,
            )
    return count

print(num_paths(set(), 'start'))
print(num_paths(set(), 'start', can_revisit_small=True))
