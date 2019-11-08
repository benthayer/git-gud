import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['octopus'], [
            'git gud commit',
            'git gud commit'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(level, commands):
    simulate(level, commands)
