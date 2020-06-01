import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['cherrypicking'], [
            'git cherry-pick bugFix',
            'git cherry-pick side~',
            'git cherry-pick another'
        ]
    ), (
        skill['interactiverebase'], [
            'git checkout overHere',
            'git checkout -b temp',
            'git cherry-pick master~2',
            'git cherry-pick master',
            'git cherry-pick master~1',
            'git branch -D master',
            'git checkout -b master',
            'git branch -d temp'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
