"""
USAGE: python check.py [EXPECTED.TXT]

Read AoC solution input from stdin, and echo it back (with a bit of decoration)
Lines starting with '*** part' are special:
 - if EXPECTED.TXT file is given, check that they appear in that file
 - output them at the end

Exit with 1 if any check failed.
"""

import sys

RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
CYAN = "\x1b[36m"
WHITE = "\x1b[37m"
RESET = "\x1b[0m"

PART_PREFIX_LEN = len('*** part N: ')

expected = {}
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            part_prefix, answer = line[:PART_PREFIX_LEN], line[PART_PREFIX_LEN:]
            print(f'{CYAN}exp.{WHITE}{part_prefix[4:]}{answer}')
            if answer:
                expected[part_prefix] = answer

failing = False
output = []

def print_expected_for_failure(failed_line):
    for exp_line, answer in expected.items():
        if exp_line.startswith(failed_line[:12]):
            print(f"{CYAN}exp.{exp_line[4:]}{WHITE}{answer}")

print(f'{CYAN}--- Starting run{WHITE}')
for line in sys.stdin:
    line = line.rstrip()
    if line.startswith('*** part'):
        failed = False
        part_prefix, answer = line[:PART_PREFIX_LEN], line[PART_PREFIX_LEN:]
        if part_prefix in expected:
            if expected[part_prefix] == answer:
                color = GREEN
            else:
                color = RED
                failed = failing = True
        else:
            color = YELLOW
        output.append((line, failed, color))
        print(f"{color}{line}{WHITE}")
        if failed:
            print_expected_for_failure(line)
    else:
        print(f'{RED if failing else YELLOW}>{WHITE}', line)

print(f'{CYAN}--- Results{WHITE}')
for line, failed, color in output:
    print(f'{color}::: {line[4:12]}{WHITE}{line[12:]}')
    if failed:
        print_expected_for_failure(line)

if failing:
    print(f'{RED}Bad result{RESET}')
    exit(1)
elif expected:
    print(f'{GREEN}All OK{RESET}')
    exit(0)
else:
    exit(0)
