import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['cherrypicking'], [
            'git cherry-pick bugFix',
            'git cherry-pick side',
            'git cherry-pick another'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)

