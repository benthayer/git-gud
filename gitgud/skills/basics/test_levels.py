import pytest

import os
import subprocess

from gitgud.operations import Operator
from . import skill


level_tests = [
    (
        skill['committing'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['branching'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['merging'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['rebasing'], [
            'git gud commit',
            'git gud commit'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_committing(level, commands):
    os.chdir('Q:/Open Source/test')
    file_operator = Operator('Q:/Open Source/test')

    level._setup(file_operator)

    for command in commands:
        subprocess.call(command, shell=True)

    assert level._test(file_operator)
