import os
from pathlib import Path
import subprocess


def write_file(filepath):
    with open(Path(filepath), "w") as newfile:
        newfile.write("{} content".format(filepath))


def simulate(gg, level, commands, run_pretest=True):
    level._setup()

    for command in commands:
        if command.startswith('{create}'):
            filename = command[len('{create} '):].strip()
            write_file(filename)
        elif '^' in command and os.name == 'nt':
            command = command.replace('^', '^^')
        # Only test if there are commands which change state.
        if run_pretest:
            assert not level._test()
        subprocess.call(command, shell=True)

    assert level._test()
