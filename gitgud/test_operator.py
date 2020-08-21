import os
import subprocess
from pathlib import Path

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
def content_level(gg):
    from gitgud.skills import all_skills
    gg.load_level(all_skills['intro']['welcome'])

    write_file("root.txt")
    os.mkdir("dir")
    write_file("dir/dirfile.txt")
    os.mkdir("dir/subdir")
    write_file("dir/subdir/subdirfile.txt")

    subprocess.call("git add .", shell=True)
    subprocess.call('git commit -m "Testing commit"', shell=True)


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


def test_file_in_commit(file_operator, content_level):
    assert not file_operator.file_in_commit("master", "welcome.txt")
    assert file_operator.file_in_commit("master", "Welcome.txt")


def test_get_commit_content(file_operator, content_level):
    assert "Welcome" in file_operator.get_commit_content("HEAD")["Welcome.txt"]  # noqa: E501
    # Check caching of decoded blob data_stream
    assert "Welcome" in file_operator.get_commit_content("HEAD")["Welcome.txt"]  # noqa: E501
    head_sha = file_operator.repo.head.commit.hexsha
    assert "Welcome" in file_operator.get_commit_content(head_sha)["Welcome.txt"]  # noqa: E501
    assert "dirfile" in file_operator.get_commit_content(head_sha)["dir/dirfile.txt"]  # noqa: E501
    # Test with path objects
    assert "subdirfile" in file_operator.get_commit_file_content(
        head_sha, Path("dir") / "subdir" / "subdirfile.txt")
    assert "dirfile" in file_operator.get_commit_file_content(
        head_sha, "dir/dirfile.txt")


def test_get_working_staging_content_tracked(file_operator, content_level):
    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()
    # Test unmodified
    assert "Welcome.txt" in staging_data
    assert staging_data["Welcome.txt"] == working_data["Welcome.txt"]
    # Test modified
    write_file("Welcome.txt")
    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()
    assert "Welcome.txt" in staging_data
    assert staging_data["Welcome.txt"] != working_data["Welcome.txt"]


def test_get_working_staging_content_untracked(file_operator, content_level):
    untracked_files = [
        "untracked.txt", "dir/untracked.txt", "dir/subdir/untracked.txt"
    ]

    for filepath in untracked_files:
        write_file(filepath)

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()

    for untracked_file in untracked_files:
        assert untracked_file in working_data
        assert untracked_file not in staging_data


def test_get_working_staging_content_added(file_operator, content_level):
    added_files = [
        "added.txt", "dir/added.txt", "dir/subdir/added.txt"
    ]

    for added_file in added_files:
        write_file(added_file)
        subprocess.call(
            "git add {}".format(Path(added_file)),
            shell=True
        )

    # Remove Welcome.txt & dirfile.txt from the working directory only
    os.unlink("Welcome.txt")
    os.unlink("dir/dirfile.txt")

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()
    commit_data = file_operator.get_commit_content("HEAD")

    for added_file in added_files:
        assert added_file in staging_data
        assert added_file in working_data

    assert staging_data["Welcome.txt"] == commit_data["Welcome.txt"]
    assert staging_data["dir/dirfile.txt"] == commit_data["dir/dirfile.txt"]
    assert "Welcome.txt" not in working_data
    assert "dir/dirfile.txt" not in working_data


def write_file(filepath):
    with open(Path(filepath), "w") as newfile:
        newfile.write("{} content".format(filepath))
