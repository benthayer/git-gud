import pytest

from git.exc import GitCommandError

from gitgud.skills import all_skills
from gitgud.operations import get_operator


@pytest.fixture(autouse=True)
def setup_level():
    all_skills["1"]["1"]._setup()
    yield


def setup_rebase_conflict():
    file_operator = get_operator()

    with open("foo", "w") as f:
        f.write("branch 1")
    file_operator.repo.index.add("foo")
    file_operator.repo.index.commit("Add a file")

    file_operator.repo.git.checkout('-b', 'branch', 'HEAD~')
    with open("foo", "w") as f:
        f.write("branch 2")
    file_operator.repo.index.add("foo")
    file_operator.repo.index.commit("Add a file")

    try:
        file_operator.repo.git.rebase('master')
    except GitCommandError:
        # This will happen every time
        pass


def setup_bisect():
    file_operator = get_operator()
    file_operator.repo.git.bisect('start')


def test_reset_during_rebase_conflict(gg):
    setup_rebase_conflict()
    all_skills["1"]["1"]._setup()


def test_reset_during_bisect(gg):
    setup_bisect()
    all_skills["1"]["1"]._setup()


def test_reset_during_bisect_then_rebase_conflict(gg):
    setup_bisect()
    setup_rebase_conflict()
    all_skills["1"]["1"]._setup()


def test_reset_during_rebase_conflict_then_bisect(gg):
    setup_rebase_conflict()
    setup_bisect()
    all_skills["1"]["1"]._setup()
