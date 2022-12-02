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
    day_dir.joinpath('expected.txt').write_text('')

subprocess.run(
    [
        'entr',
        '-ccs', f"""
            echo Day {day_num:02}
            python day.py < smallinput.txt | python ../check.py expected.txt
            python day.py < input.txt | python ../check.py
        """
    ],
    cwd=day_dir,
    input='day.py\ninput.txt\nsmallinput.txt\nexpected.txt',
    encoding='utf-8',
)
