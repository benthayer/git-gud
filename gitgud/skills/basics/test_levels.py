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
            'git checkout -b bugFix',
            'git gud commit'
        ]
    ), (
        skill['merging'], [
            'git checkout -b bugFix',
            'git gud commit',
            'git checkout master',
            'git gud commit',
            'git merge bugFix'
        ]
    ), (
        skill['rebasing'], [
            'git rebase master bugFix'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
