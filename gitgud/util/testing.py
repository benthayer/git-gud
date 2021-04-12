import os
from pathlib import Path
import subprocess


def write_file(filepath):
    with open(Path(filepath), "w") as newfile:
        newfile.write("{} content".format(filepath))


def simulate(gg, level, commands, run_pretest=True):
    level._setup()

    for command in commands:
        command = command.strip()
        if len(command) == 0 or command[0] == '#':
            continue
        # Only test if there are commands which change state.
        if run_pretest:
            assert not level._test()

        print(f'Calling command: {command}')
        if command.startswith('{create}'):
            filename = command[len('{create} '):].strip()
            write_file(filename)
        elif '^' in command and os.name == 'nt':
            command = command.replace('^', '^^')
        subprocess.call(command, shell=True)

    assert level._test()
