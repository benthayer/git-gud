import pytest

from gitgud.util.testing import simulate

from . import skill


level_tests = [
    (skill['welcome'], skill['welcome'].solution_list(), True),
    (skill['config'], skill['config'].solution_list(), False),
    (skill['init'], skill['init'].solution_list(), True),
]


@pytest.mark.parametrize('level,commands,run_pretest', level_tests)
def test_level(gg, level, commands, run_pretest):
    simulate(gg, level, commands, run_pretest)
