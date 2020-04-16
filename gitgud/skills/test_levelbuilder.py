import os

from gitgud.skills import all_skills
from gitgud.skills.util import NamedList, Skill
from gitgud.skills.level_builder import Level


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


def test_instructions():
    for skill in all_skills:
        for level in skill:
            os.path.isfile(level.instructions_path)


def test_goal():
    for skill in all_skills:
        for level in skill:
            os.path.isfile(level.goal_path)


def test_init_NL():
    nltest = NamedList(['foo', 'bar'], [511, 522])


def test_getitem_NL():
    nltest = NamedList(['foo', 'bar', 'baz'], [5, 7, 9])
    assert nltest['1'] == 5
    assert nltest['baz'] == 9


def test_iter_NL():
    ['' for skill in all_skills]


def test_len_NL():
    nltest = NamedList(['foo', 'bar', 'baz'], [51, 72, 93])
    assert len(nltest) == 3


def test_setitem_NL():
    nltest = NamedList(['foo', 'bar', 'baz'], [51, 72, 93])
    nltest['qux'] = -21
    assert nltest['qux'] == -21


def test_contains_NL():
    assert all_skills['1'] in all_skills
    assert all_skills['1']['1'] in all_skills['1']
