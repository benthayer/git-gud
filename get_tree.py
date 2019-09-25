from git import Repo
from collections import deque


def get_change(commit):
    pass


def create_tree():
    # TODO Assert that there are no changes within the commits???
    # TODO Find changes in commit
    # TODO What does a merge commit look like - just has multiple parents

    repo = Repo('.')

    commit_queue = deque()

    for branch in repo.branches:
        # reverse from all tags, branches etc
        commit_queue.append(branch.commit)

    for tag in repo.tags:
        commit_queue.append(tag.commit)

    all_commits = {}
    while len(commit_queue) != 0:
        commit = commit_queue.popleft()
        if commit.hexsha in all_commits:
            continue
        all_commits[commit.hexsha] = commit
        for parent in commit.parents:
            commit_queue.append(parent)

    # TODO Name changes - are git difs all the same?
    # Name after the file changed or after the


if __name__ == '__main__':
    create_tree()