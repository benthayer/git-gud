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
    assert file_operator.get_level_progress(level) in {
        "unvisited", "visited", "partial", "complete"
    }


def test_update_progress_file(file_operator, progress_data):
    file_operator.read_progress_file()
    level = all_skills["1"]["1"]
    progress_data[level.skill.name].update({level.name: "value"})
    file_operator.update_progress_file(progress_data)
    assert file_operator.get_level_progress(level) == "value"
    assert file_operator.get_level_progress(level.next_level) == "unvisited"


def test_mark_level_visited(file_operator):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level_visited(level)
    assert file_operator.get_level_progress(level) == "visited"


def test_mark_level_complete(file_operator):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level_complete(level)
    assert file_operator.get_level_progress(level) == "complete"


def test_mark_level_partial(file_operator):
    level = all_skills["1"]["1"]
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level_partial(level)
    assert file_operator.get_level_progress(level) == "partial"
