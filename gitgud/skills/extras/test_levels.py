import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['octopus'], [
            'git merge feature1 feature2'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
