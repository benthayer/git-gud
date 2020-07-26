import pytest

from gitgud.skills import all_skills
from gitgud.operations import get_operator


@pytest.fixture
def file_operator(gg):
    file_operator = get_operator()
    assert file_operator is not None
    return file_operator


@pytest.fixture(scope='function')
def progress_data(file_operator, gg):
    progress_data = file_operator.read_progress_file()
    return progress_data


def test_get_level_progress(file_operator, progress_data):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) in {"complete", "incomplete", "unvisited"}  # noqa: E501


def test_update_progress_file(file_operator, progress_data):
    file_operator.read_progress_file()
    level = all_skills["1"]["1"]
    progress_data[level.skill.name].update({level.name: "incomplete"})
    file_operator.update_progress_file(progress_data)
    assert file_operator.get_level_progress(level) == "incomplete"
    assert file_operator.get_level_progress(level.next_level) == "unvisited"


def test_mark_level_incomplete(file_operator):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level_incomplete(level)
    assert file_operator.get_level_progress(level) == "incomplete"


def test_mark_level_complete(file_operator):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level_complete(level)
    assert file_operator.get_level_progress(level) == "complete"
