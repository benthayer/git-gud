import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        # User would use something like "git checkout a1b2c3d4"
        skill['detaching'], [
            'git checkout bugFix',
            'git checkout @^',
            'git checkout @{1}',
        ]
    ), (
        skill['relrefs1'], [
            'git checkout HEAD^2'
        ]
    ), (
        skill['relrefs2'], [
            'git checkout bugFix~2'
        ]
    ), (
        skill['reversing'], [
            'git reset HEAD~ --hard',
            'git checkout remote',
            'git revert HEAD^2~~..HEAD^2'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
