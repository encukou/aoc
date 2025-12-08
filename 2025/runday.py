"""
Run the daily script for day given as argument.
(Create the directory structure if it doesn't exist yet.)

Reqiures the `entr` command.
"""

from pathlib import Path
import sys
import subprocess

day_num = int(sys.argv[1])

day_dir = Path(f'{day_num:02}')
is_advent_day = (0 < day_num <= 25)
if not day_dir.exists() and is_advent_day:
    day_dir.mkdir(exist_ok=True)
    template = Path('template.py').read_text()
    day_dir.joinpath('day.py').write_text(template)
    day_dir.joinpath('input.txt').write_text('')
    day_dir.joinpath('smallinput.txt').write_text('')
    day_dir.joinpath('expected.txt').write_text('*** part 1: \n*** part 2: ')

subprocess.run(
    [
        'entr',
        '-rccs', f"""
            echo Day {day_num:02}
            set -e -o pipefail
            SMALL=1 python day.py < smallinput.txt  2>&1 | python ../check.py expected.txt
            time python day.py < input.txt  2>&1 | python ../check.py
        """
    ],
    cwd=day_dir,
    input='day.py\ninput.txt\nsmallinput.txt\nexpected.txt',
    encoding='utf-8',
)
