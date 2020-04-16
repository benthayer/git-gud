import pytest

from . import skill

from gitgud.skills import all_levels
from gitgud.skills.parsing import parse_spec

@pytest.mark.parametrize('level', all_levels)
def test_setup_spec_has_no_duplicate_commits(level):
    commits = parse_spec(level.setup_spec_path)[0]
    names = [commit[0] for commit in commits]
    assert len(names) == len(set(names))

@pytest.mark.parametrize('level', all_levels)
def test_test_spec_has_no_duplicate_commits(level):
    commits = parse_spec(level.test_spec_path)[0]
    names = [commit[0] for commit in commits]
    assert len(names) == len(set(names))

