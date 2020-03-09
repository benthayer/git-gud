import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['intro'], [
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
