import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['{}'], [
            'git gud commit',  # Example, change to solution for your level"
            'git merge example'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
