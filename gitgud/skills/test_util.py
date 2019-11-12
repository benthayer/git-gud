import os

from gitgud.skills import all_skills
from gitgud.skills.util import Skill, Level, NamedList


def test_access():
    all_skills[0]
    all_skills['basics']
    all_skills['basics'][0]
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

def test_contains():
    assert all_skills.contains(all_skills[1])
    assert all_skills[1].contains(all_skills[1][2])

def test_len():
    assert len(all_skills[0]) == 4

