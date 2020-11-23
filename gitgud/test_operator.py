import os
import subprocess
from pathlib import Path

import pytest

from gitgud.operations import get_operator
from gitgud.util.testing import write_file
from gitgud.user_messages.stateful import display_commit_content
from gitgud.user_messages.stateful import display_working_directory_content
from gitgud.user_messages.stateful import display_staging_area_content


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


def test_update_progress_file(file_operator, level):
    progress_data = {
        level.skill.name: {
            level.name: "value"
        }
    }
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


def test_get_commit_content(file_operator, content_level):
    head = file_operator.repo.head.commit
    commit_content = file_operator.get_commit_content(head)

    assert "Welcome" in commit_content["Welcome.txt"]
    assert "dirfile" in commit_content["dir/dirfile.txt"]
    assert "subdirfile" in commit_content["dir/subdir/subdirfile.txt"]

    assert "Welcome" in commit_content[Path("Welcome.txt")]
    assert "dirfile" in commit_content[Path("dir/dirfile.txt")]
    assert "subdirfile" in commit_content[Path("dir/subdir/subdirfile.txt")]


def test_get_commit_content_caching(file_operator, content_level):
    content1 = file_operator.get_commit_content("HEAD")
    content2 = file_operator.get_commit_content("HEAD")

    assert "Welcome" in content1["Welcome.txt"]
    assert "Welcome" in content2["Welcome.txt"]

    head = file_operator.repo.head.commit
    content3 = file_operator.get_commit_content(head)
    content4 = file_operator.get_commit_content(head)

    assert "Welcome" in content3["Welcome.txt"]
    assert "Welcome" in content4["Welcome.txt"]

    assert content1 == content2 == content3 == content4


def test_get_commit_content_contains(file_operator, content_level):
    head = file_operator.repo.head.commit
    commit_content = file_operator.get_commit_content(head)

    assert "Welcome.txt" in commit_content
    assert "dir/dirfile.txt" in commit_content

    assert Path("Welcome.txt") in commit_content
    assert Path("dir/dirfile.txt") in commit_content


def test_unmodified_content(file_operator, content_level):
    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()

    # Test unmodified
    assert "Welcome.txt" in staging_data
    assert staging_data["Welcome.txt"] == working_data["Welcome.txt"]


def test_modified_content(file_operator, content_level):
    # Test modified
    write_file("Welcome.txt")
    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()

    assert "Welcome.txt" in staging_data
    assert staging_data["Welcome.txt"] != working_data["Welcome.txt"]


def test_untracked_content(file_operator, content_level):
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


def test_removed_content(file_operator, content_level):
    # Remove Welcome.txt & dirfile.txt from the working directory only
    os.unlink("Welcome.txt")
    os.unlink("dir/dirfile.txt")

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()
    commit_data = file_operator.get_commit_content("HEAD")

    assert staging_data["Welcome.txt"] == commit_data["Welcome.txt"]
    assert staging_data["dir/dirfile.txt"] == commit_data["dir/dirfile.txt"]
    assert "Welcome.txt" not in working_data
    assert "dir/dirfile.txt" not in working_data


def test_added_content(file_operator, content_level):
    added_files = [
        "added.txt", "dir/added.txt", "dir/subdir/added.txt"
    ]

    for added_file in added_files:
        write_file(added_file)
        file_operator.repo.git.add(Path(added_file))

    staging_data = file_operator.get_staging_content()
    working_data = file_operator.get_working_directory_content()

    for added_file in added_files:
        assert added_file in staging_data
        assert added_file in working_data


def test_get_all_commits(file_operator, content_level):
    # Check for consistency
    commits1 = list(file_operator.get_all_commits())
    commits2 = list(file_operator.get_all_commits())
    assert commits1 == commits2


def test_commit_messages(file_operator, content_level):
    display_staging_area_content()
    display_working_directory_content()
    display_commit_content()
