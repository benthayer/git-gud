import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['{}'], [# Examples, change to solution for your level"
            'git gud commit',
            'git gud commit',
            'git checkout HEAD^',
            'git checkout -b changes-to-be-made-by-player',
            'git checkout checked-out-branch'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)

