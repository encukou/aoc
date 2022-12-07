import sys

data = sys.stdin.read().splitlines()
print(data)


class Dir:
    def __init__(self, name, parent):
        self._contents = {}
        self._total_size = 0
        self.name = name
        self.parent = parent

    def __repr__(self):
        return f'<Dir {self.name}>'

    def add_subdir(self, name):
        return self._contents.setdefault(name, Dir(name, self))

    def ls_add(self, name, size):
        if name not in self._contents:
            self._contents[name] = size
            parent = self
            while parent:
                parent._total_size += size
                parent = parent.parent

    def walk(self, indent=0):
        print('  ' * indent, self.name, '(dir)', self._total_size)
        yield self
        for name, entry in self._contents.items():
            if isinstance(entry, Dir):
                yield from entry.walk(indent+1)
            else:
                print('  ' * (indent+1), name, entry)

root = Dir('/', None)
path = [root]
for line in data:
    parts = line.split()
    print(parts)
    match parts:
        case '$', 'cd', '..':
            path.pop()
        case '$', 'cd', '/':
            del path[1:]
        case '$', 'cd', name:
            path.append(path[-1].add_subdir(name))
        case '$', 'ls':
            pass
        case 'dir', name:
            path[-1].add_subdir(name)
        case size, name:
            path[-1].ls_add(name, int(size))
        case _:
            raise ValueError(parts)

    for d in root.walk():
        pass

small_dir_total = 0
candidates = []
unused = 70000000 - root._total_size
NEED_TO_FREE = 30000000 - unused
print(f'{unused=}')
print(f'{NEED_TO_FREE=}')
for d in root.walk():
    if d._total_size <= 100000:
        small_dir_total += d._total_size
    if d._total_size >= NEED_TO_FREE:
        candidates.append(d)
candidates.sort(key=lambda d: d._total_size)
print(candidates)

print('*** part 1:', small_dir_total)
print('*** part 2:', candidates[0]._total_size)
# not 43629016
