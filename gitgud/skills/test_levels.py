import pytest

from gitgud.skills import all_skills, all_levels
from gitgud.skills.level_builder import Level, BasicLevel
from gitgud.skills.util import Skill
from gitgud.skills.parsing import parse_spec


def test_skill_access():
    all_skills['1']
    all_skills['basics']
    all_skills['basics']['1']
    all_skills['basics']['committing']


def test_types():
    for skill in all_skills:
        assert isinstance(skill, Skill)
        for level in skill:
            assert isinstance(level, Level)


def test_explain():
    for skill in all_skills:
        for level in skill:
            if level.explain.__code__ == BasicLevel.explain.__code__:
                assert level.file('explanation.txt').is_file()


def test_goal():
    for level in all_levels:
        if level.goal.__code__ == BasicLevel.goal.__code__:
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
