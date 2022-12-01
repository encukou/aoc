from pathlib import Path
import sys
import subprocess

day_num = int(sys.argv[1])

day_dir = Path(f'{day_num:02}')
if not day_dir.exists():
    day_dir.mkdir(exist_ok=True)
    template = Path('template.py').read_text()
    day_dir.joinpath('day.py').write_text(template)
    day_dir.joinpath('input.txt').write_text(template)

subprocess.run(
    [
        'entr',
        '-ccs', f"""
            echo Day {day_num:02}
            PS4='———— '
            set -ex
            env SMALLDATA=1 python day.py
            python day.py
        """
    ],
    cwd=day_dir,
    input='day.py\ninput.txt',
    encoding='utf-8',
)
