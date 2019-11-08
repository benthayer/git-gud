import os
import subprocess

from gitgud.operations import Operator


def simulate(level, commands):
    os.chdir('Q:/Open Source/test')
    file_operator = Operator('Q:/Open Source/test')

    level._setup(file_operator)

    for command in commands:
        subprocess.call(command, shell=True)

    assert level._test(file_operator)
