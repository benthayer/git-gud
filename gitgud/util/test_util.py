import pytest
from gitgud.util import NamedList


@pytest.fixture
def named_list():
    return NamedList(['foo', 'bar', 'baz'], [51, 72, 93])


@pytest.fixture
def all_skills(scope="module"):
    from gitgud.skills import all_skills
    return all_skills


def test_getitem_NL(named_list):
    assert named_list['1'] == 51
    assert named_list['baz'] == 93


def test_len_NL(named_list):
    assert len(named_list) == 3


def test_setitem_NL(named_list):
    named_list['qux'] = -21
    assert named_list['qux'] == -21


def test_contains_AS(all_skills):
    assert all_skills['1'] in all_skills
    assert all_skills['1']['1'] in all_skills['1']


def test_iter_AS(all_skills):
    for skill in all_skills:
        pass


def test_index_NL():
    named_list = NamedList(['foo', 'bar', 'baz'], [51, 72, 93], start_index=3)
    assert named_list.index('foo') == '3'
    assert named_list.index('baz') == '5'
