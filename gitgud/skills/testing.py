import os
import subprocess


def simulate(gg, level, commands):
    level._setup(gg.file_operator)

    for command in commands:
        if '^' in command and os.name == 'nt':
            command = command.replace('^', '^^')
        subprocess.call(command, shell=True)

    assert level._test(gg.file_operator)
