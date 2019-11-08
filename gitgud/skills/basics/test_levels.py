import pytest

from gitgud.skills.testing import simulate

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
def test_level(level, commands):
    simulate(level, commands)
