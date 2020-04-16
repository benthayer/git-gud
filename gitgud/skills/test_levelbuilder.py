import os

from gitgud.skills import all_skills, all_levels
from gitgud.skills.util import NamedList, Skill
from gitgud.skills.level_builder import Level


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
