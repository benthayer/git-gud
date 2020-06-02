import pytest

from gitgud.skills.testing import simulate

from . import skill


level_tests = [
    (
        skill['welcome'], [
        ]
    ), (
        skill['config'], [
            'git config user.name "Git Gud Test"',
            'git config user.email "ggtest@example.com"'
        ]
    )
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
