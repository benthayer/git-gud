import os
import subprocess
from gitgud import operations


def simulate(gg, level, commands):

    operations._operator = None

    level._setup()

    for command in commands:
        if '^' in command and os.name == 'nt':
            command = command.replace('^', '^^')
        subprocess.call(command, shell=True)

    operations._operator = None
    assert level._test()
