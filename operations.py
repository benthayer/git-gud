import os
import shutil

from git import Repo
from git import Head
from git import Actor
from git.exc import NoSuchPathError
from git.exc import GitCommandError


def add_file_to_index(index, filename):
    # TODO Want to do this in the working directory
    # TODO Use tree only when in dev-mode
    open(f'tree/{filename}', 'w+').close()
    index.add([filename])


def add_and_commit(name):
    repo = Repo('tree') # TODO Use tree only whe in dev mode
    index = repo.index
    add_file_to_index(index, name)
    author = Actor("Git Gud", "git-gud@example.com")
    return index.commit(name, author=author, committer=author)


class Commit:
    def __init__(self, name):
        self.name = name
        self.children = []


def get_branching_tree(tree):
    # TODO Delete this function and Commit class
    commits = {}

    for commit in tree['commits']:
        for parent in commit['parents']:
            if parent not in commits:
                commits[parent] = Commit(parent)
            commits[parent].children.append(commit)

    return commits


def delete_files():
    # TODO Only use tree in dev-mode
    for file in os.listdir('tree'):
        file_path = os.path.join('tree', file)
        if file == '.git':
            continue
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def create_tree(commits, head):

    try:
        repo = Repo('tree')
    except NoSuchPathError:
        repo = Repo.init('tree') # TODO Only use tree in dev-mode
        repo.init()

    index = repo.index
    delete_files()
    index.commit("Clearing index")  # Easiest way to clear the index is to commit an empty directory


    # Switch to temp first in case git-gud-construction exists
    if repo.head.reference.name != 'temp':
        repo.head.reference = Head(repo, 'refs/heads/temp')

    # Delete git-gud-construction so we can guarantee it's an orphan
    try:
        repo.delete_head('git-gud-construction')
    except GitCommandError:
        pass  # Branch doesn't exist

    repo.head.reference = Head(repo, 'refs/heads/git-gud-construction')
    try:
        repo.delete_head('temp')
    except GitCommandError:
        pass # If temp didn't exist, we only checked it out as an orphan, so it already disappeared

    for branch in repo.branches:
        if branch.name != 'git-gud-construction':
            repo.delete_head(branch, force=True)
    repo.delete_tag(*repo.tags)

    index = repo.index
    author = Actor("Git Gud", "git-gud@example.com")
    commit_objects = {}

    for name, parents, branches, tags in commits:
        # commit = (name, parents, branches, tags)
        parents = [commit_objects[parent] for parent in parents]
        if parents:
            repo.active_branch.set_commit(parents[0])
        if len(parents) < 2:
            # Not a merge
            add_file_to_index(index, name)
        commit = index.commit(name, author=author, committer=author, parent_commits=parents)
        commit_objects[name] = commit

        for branch in branches:
            repo.create_head(branch, commit)

        for tag in tags:
            repo.create_tag(tag, commit)
        # TODO Log commit hash and info

    # TODO Checkout using name
    for branch in repo.branches:
        if branch.name == head:
            branch.checkout()

    repo.delete_head('git-gud-construction')