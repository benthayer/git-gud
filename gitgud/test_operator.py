import os
import subprocess

import pytest

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


@pytest.fixture
def content_level():
    from gitgud.skills import all_skills
    # TODO: Make a proper testing level with details.yaml
    # We're using intro/welcome because it specifies a details.yaml
    return all_skills['intro']['welcome']


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


def test_file_in_commit(file_operator, gg, content_level):
    gg.load_level(content_level)
    assert not file_operator.file_in_commit("master", "welcome.txt")
    assert file_operator.file_in_commit("master", "Welcome.txt")


def test_get_commit_file_content(file_operator, gg, content_level):
    gg.load_level(content_level)
    assert "Welcome" in file_operator.get_commit_file_content("HEAD", "Welcome.txt")  # noqa: E501
    # Check caching of decoded blob data_stream
    assert "Welcome" in file_operator.get_commit_file_content("HEAD", "Welcome.txt")  # noqa: E501
    head_sha = file_operator.repo.head.commit.hexsha
    assert "Welcome" in file_operator.get_commit_file_content(head_sha, "Welcome.txt")  # noqa: E501


def test_get_working_staging_content(file_operator, gg, content_level):
    gg.load_level(content_level)
    assert "untracked.txt" not in file_operator.get_working_content()

    with open("untracked.txt", "w"):
        pass

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_content()

    assert "untracked.txt" in working_data
    assert "untracked.txt" not in staging_data

    assert "Welcome.txt" in staging_data
    assert staging_data["Welcome.txt"] == working_data["Welcome.txt"]

    # Add untracked.txt to the index
    subprocess.call("git add untracked.txt", shell=True)
    # Remove Welcome.txt from the working directory, but don't add to index
    os.unlink("Welcome.txt")

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_content()
    commit_content = \
        file_operator.get_commit_file_content("HEAD", "Welcome.txt")

    assert staging_data["Welcome.txt"] == commit_content

    assert "untracked.txt" in staging_data, staging_data
    assert "untracked.txt" in working_data, working_data
