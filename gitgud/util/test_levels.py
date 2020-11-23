import pytest

from gitgud.skills import all_skills, all_levels
from gitgud.util.level_builder import Level, BasicLevel
from gitgud.util import Skill
from gitgud.util.parsing import parse_spec


def test_skill_access():
    all_skills['1']
    all_skills['basics']
    all_skills['basics']['1']
    all_skills['basics']['committing']


@pytest.mark.parametrize('skill', all_skills)
def test_skill_types(skill):
    assert isinstance(skill, Skill)


@pytest.mark.parametrize('level', all_levels)
def test_level_types(level):
    assert isinstance(level, Level)


@pytest.mark.parametrize('level', all_levels)
def test_explain(level):
    if level.explain.__func__ == BasicLevel.explain:
        assert level.file('explanation.txt').is_file()


@pytest.mark.parametrize('level', all_levels)
def test_goal(level):
    if level.goal.__func__ == BasicLevel.goal:
        assert level.file('goal.txt').is_file()


@pytest.mark.parametrize('level', all_levels)
def test_setup_spec_has_no_duplicate_commits(level):
    if not level.file('setup.spec').exists():
        return
    commits = parse_spec(level.file('setup.spec'))[0]
    names = [commit[0] for commit in commits]
    assert len(names) == len(set(names))


@pytest.mark.parametrize('level', all_levels)
def test_test_spec_has_no_duplicate_commits(level):
    if not level.file('test.spec').exists():
        return
    commits = parse_spec(level.file('test.spec'))[0]
    names = [commit[0] for commit in commits]
    assert len(names) == len(set(names))


@pytest.mark.parametrize('level', all_levels)
def test_rebases_have_originals(level):
    if not (
            level.file('setup.spec').exists() and
            level.file('test.spec').exists()):
        return
    setup_commits = parse_spec(level.file('setup.spec'))[0]
    test_commits = parse_spec(level.file('test.spec'))[0]
    all_commits = setup_commits + test_commits

    names = [commit[0] for commit in all_commits]

    rebases = [name for name in names if name[-1] == "'"]

    for rebase in rebases:
        assert rebase[:-1] in names
