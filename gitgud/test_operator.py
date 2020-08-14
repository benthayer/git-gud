import pytest
import random

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


@pytest.fixture(scope='module')
def level():
    from gitgud.skills import all_skills
    return all_skills["1"]["1"]


def test_get_level_progress(file_operator, progress_data, level):
    assert file_operator.get_level_progress(level) in {
        "unvisited", "visited", "partial", "complete"
    }


def test_update_progress_file(file_operator, progress_data, level):
    file_operator.read_progress_file()
    progress_data[level.skill.name].update({level.name: "value"})
    file_operator.update_progress_file(progress_data)
    assert file_operator.get_level_progress(level) == "value"
    assert file_operator.get_level_progress(level.next_level) == "unvisited"


def test_mark_level_visited(file_operator, level):
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level(level, "visited")
    assert file_operator.get_level_progress(level) == "visited"


def test_mark_level_complete(file_operator, level):
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level(level, "complete")
    assert file_operator.get_level_progress(level) == "complete"


def test_mark_level_partial(file_operator, level):
    assert file_operator.get_level_progress(level) == "unvisited"
    file_operator.mark_level(level, "partial")
    assert file_operator.get_level_progress(level) == "partial"

def test_mark_level_hierarchy(file_operator, level):
    hierarchy = [
        "unvisited", "visited", "partial", "complete"
    ]
    for index, status in enumerate(hierarchy):
        file_operator.mark_level(level, status)
        for weaker in hierarchy[index::-1]:
            initial_status = level.get_progress()
            file_operator.mark_level(level, weaker)
            assert initial_status == level.get_progress()
