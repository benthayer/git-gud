import os
import subprocess

from gitgud.operations import Operator


def simulate(level, commands):
    # TODO Move the test dir to a temporary directory that will always be accessible
    test_dir = 'Q:/Open Source/test'
    os.chdir(test_dir)
    file_operator = Operator(test_dir)

    level._setup(file_operator)

    for command in commands:
        subprocess.call(command, shell=True)

    assert level._test(file_operator)
