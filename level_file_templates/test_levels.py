import pytest

from gitgud.util.testing import simulate

from . import skill


level_tests = [
    (level, level.solution_list()) for level in skill
]


@pytest.mark.parametrize('level,commands', level_tests)
def test_level(gg, level, commands):
    simulate(gg, level, commands)
