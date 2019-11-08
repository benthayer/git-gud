import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['detaching'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['relrefs1'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['relrefs2'], [
            'git gud commit',
            'git gud commit'
        ]
    ), (
        skill['reversing'], [
            'git gud commit',
            'git gud commit'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(level, commands):
    simulate(level, commands)
