import collections
import random
import sys
import os

data = sys.stdin.read().splitlines()
print(data)

def init(data):
    devices_to_outputs = collections.defaultdict(list)
    for line in data:
        label, outputs = line.split(':')
        outputs = outputs.strip().split()
        devices_to_outputs[label] = outputs
    devices_to_outputs['out'] = []
    return devices_to_outputs

def find_n_paths(devices_to_outputs, src='you', dest='out', omit=(), delay=0):
    n_paths = {d: 0 for d in devices_to_outputs}
    to_visit = collections.defaultdict(int)
    to_visit[src] = 1
    while to_visit:
        device = random.choice(list(to_visit.keys()))
        n = to_visit.pop(device)
        if device in omit:
            continue
        n_paths[device] += n
        print(f'({len(to_visit)}) {device}: {n:+} → {n_paths[device]}', flush=True)
        if device != dest:
            for output in devices_to_outputs[device]:
                to_visit[output] += n
        import time
        #time.sleep(delay)
    return n_paths[dest]

print('*** part 1:', find_n_paths(init(data)))

if 'SMALL' in os.environ:
    data = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip().splitlines()

devices_to_outputs = init(data)
svr_to_fft = find_n_paths(devices_to_outputs, 'svr', 'fft', {'dac'}, delay=.1)
svr_to_dac = find_n_paths(devices_to_outputs, 'svr', 'dac', {'fft'})
fft_to_dac = find_n_paths(devices_to_outputs, 'fft', 'dac')
dac_to_fft = find_n_paths(devices_to_outputs, 'dac', 'fft')
dac_to_out = find_n_paths(devices_to_outputs, 'dac', 'out')
fft_to_out = find_n_paths(devices_to_outputs, 'fft', 'out')
print(f'{svr_to_fft=} {svr_to_dac=} {fft_to_dac=} {dac_to_fft=} {dac_to_out=} {fft_to_out=}')


print('*** part 2:', svr_to_fft*fft_to_dac*dac_to_out + svr_to_dac*dac_to_fft*fft_to_out)
