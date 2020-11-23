from gitgud.util.parsing import branches_to_lowercase
from gitgud.skills import all_skills
from gitgud.util.testing import simulate


def test_lowercase_level(gg):
    level = all_skills['basics']['branching']
    commands1 = [
        'git checkout -b bugFix',
        'git gud commit'
    ]
    commands2 = [
        'git checkout -b bugfix',
        'git gud commit'
    ]
    simulate(gg, level, commands1, run_pretest=False)
    simulate(gg, level, commands2, run_pretest=False)


def test_branches_to_lowercase():
    branch = {
        'target': 'fake_commit',
        'id': 'UPPERBRANCH'
    }

    level_tree = {
        'branches': {'UPPERBRANCH': branch},
        'HEAD': {'target': 'UPPERBRANCH', 'id': 'HEAD'}
    }
    test_tree = {
        'branches': {'UPPERBRANCH': branch, 'MASTER': 'string'},
        'HEAD': {'target': 'UPPERBRANCH', 'id': 'HEAD'}
    }
    setup_tree = {
        'branches': {'MASTER': 'string'},
        'HEAD': {'target': 'MASTER', 'id': 'HEAD'}
    }

    branches_to_lowercase(level_tree, setup_tree, test_tree)

    assert 'UPPERBRANCH' not in level_tree['branches']
    assert 'upperbranch' in level_tree['branches']
    assert level_tree['branches']['upperbranch'] is branch
    assert level_tree['HEAD']['target'] == 'upperbranch'

    assert 'UPPERBRANCH' not in test_tree['branches']
    assert 'upperbranch' in test_tree['branches']
    assert test_tree['branches']['upperbranch'] is branch
    assert test_tree['HEAD']['target'] == 'upperbranch'

    assert 'MASTER' in test_tree['branches']
    assert 'MASTER' in setup_tree['branches']
    assert setup_tree['HEAD']['target'] == 'MASTER'
