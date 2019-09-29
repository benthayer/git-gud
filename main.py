from argparse import ArgumentParser

import os
import shutil

from git import Repo
from git import Head
from git import Actor
from git.exc import NoSuchPathError
from git.exc import GitCommandError


def parse_tree(tree_str):
    # The purpose of this method is to get a more computer-readable commit tree

    commits = []  # List of  (commit_name, [parents], [branches], [tags])
    all_branches = set()
    all_tags = set()

    for line in tree_str.split('\n'):
        if line[0] == '#':
            continue
        line = line.replace('  ', '')

        if '(' in line:
            commit_str = line[:line.find('(')].strip()
            ref_str = line[line.find('(')+1:-1].strip().replace(' ', '')
        else:
            commit_str = line.strip()
            ref_str = ''

        if ':' not in commit_str:
            # Implicit parent, use previous commit
            if len(commits) == 0:
                parents = []
            else:
                parents = [commits[len(commits)-1][0]]
            commit_name = commit_str
        else:
            # Find parent
            commit_name, parent_str = commit_str.split(':')
            commit_name = commit_name.strip()
            parent_str = parent_str.strip()

            if parent_str:
                parents = parent_str.split(' ')
            else:
                parents = []

        # We know the commit name and parents now

        assert ' ' not in commit_name  # There should never be more than one change or a space in a name

        # Process references
        if ref_str:
            refs = ref_str.split(',')
        else:
            refs = []
        branches = []
        tags = []
        for ref in refs:
            if ref[:4] == 'tag:':
                tag = ref[4:]
                assert tag not in all_tags
                tags.append(tag)
                all_tags.add(tag)
            else:
                branch = ref
                assert branch not in all_branches
                branches.append(branch)
                all_branches.add(branch)
        commits.append((commit_name, parents, branches, tags))

    head = commits[-1][0]
    del commits[-1]

    return commits, head


def level_json(commits, head):
    # We've formally replicated the input string in memory

    level = {
        'topology': [],
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    all_branches = []
    all_tags = []
    for commit_name, parents, branches_here, tags_here in commits:
        level['topology'].append(commits)
        level['commits'][commit_name] = {
            'parents': parents,
            'id': commit_name
        }
        if not parents:
            level['commits'][commit_name]['rootCommit'] = True
        all_branches.extend(branches_here)
        all_tags.extend(tags_here)

        for branch in branches_here:
            level['branches'][branch] = {
                'target': commit_name,
                'id': branch
            }

        for tag in tags_here:
            level['tags'][tag] = {
                'target': commit_name,
                'id': tag
            }

    level['HEAD'] = {
        'target': head,
        'id': 'HEAD'
    }

    return level


def add_file_to_index(index, filename):
    # TODO Want to do this in the working directory
    # TODO Use tree only when in dev-mode
    open(f'tree/{filename}', 'w+').close()
    index.add([filename])


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
    pass
    # TODO delete git-gud-construction


# TODO Commit
# TODO Test
# TODO Save
# TODO Load
# TODO Instructions
# TODO convert commit tree into spec format
# TODO convert spec format into commit tree

def main():
    with open('spec.spec') as spec_file:
        commits, head = parse_tree(spec_file.read())
        create_tree(commits, head)

    pass


if __name__ == '__main__':
    main()
