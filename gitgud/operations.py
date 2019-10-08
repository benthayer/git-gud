import os
import shutil

from git import Repo
from git import Head

from git.exc import GitCommandError
from git.exc import InvalidGitRepositoryError

from gitgud import actor


class Operator:
    def __init__(self, path, initialize=False):
        self.path = path
        self.repo = None

        if initialize:
            self.initialize()

        self.git_path = os.path.join(self.path, '.git')
        self.gg_path = os.path.join(self.git_path, 'gud')
        self.last_commit_path = os.path.join(self.gg_path, 'last_commit')
        self.level_path = os.path.join(self.gg_path, 'level')

    def initialize(self):
        try:
            self.repo = Repo(os.getcwd())
        except InvalidGitRepositoryError:
            self.repo = Repo.init(os.getcwd())

    def add_file_to_index(self, filename):
        open(f'{self.path}/{filename}', 'w+').close()
        self.repo.index.add([filename])

    def add_and_commit(self, name):
        # TODO Commits with the same time have arbitrary order when using git log, set time of commit to fix
        self.add_file_to_index(name)
        commit = self.repo.index.commit(name, author=actor, committer=actor)

        return commit

    def delete_files(self):
        for file in os.listdir(self.path):
            file_path = os.path.join(self.path, file)
            if file == '.git':
                continue
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def create_tree(self, commits, head):
        repo = self.repo
        index = repo.index

        self.delete_files()
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
            pass  # If temp didn't exist, we only checked it out as an orphan, so it already disappeared

        for branch in repo.branches:
            if branch.name != 'git-gud-construction':
                repo.delete_head(branch, force=True)
        repo.delete_tag(*repo.tags)

        index = repo.index
        commit_objects = {}

        for name, parents, branches, tags in commits:
            # commit = (name, parents, branches, tags)
            parents = [commit_objects[parent] for parent in parents]
            if parents:
                repo.active_branch.set_commit(parents[0])
            if len(parents) < 2:
                # Not a merge
                self.add_file_to_index(name)
            commit = index.commit(name, author=actor, committer=actor, parent_commits=parents)
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

    def get_current_tree(self):
        # Return a json object with the same structure as in level_json

        repo = self.repo

        tree = {
            'branches': {},  # 'branch_name': {'target': 'commit_id', 'id': 'branch_name'}
            'tags': {},  # 'branch_name': {'target': 'commit_id', 'id': 'branch_name'}
            'commits': {},  # '2': {'parents': ['1'], 'id': '1'}
            'HEAD': {}  # 'target': 'branch_name', 'id': 'HEAD'
        }

        commits = set()
        visited = set()

        for branch in repo.branches:
            commits.add(branch.commit)
            commit_name = branch.commit.message.strip()
            tree['branches'][branch.name] = {
                "target": commit_name,
                "id": branch.name
            }

        for tag in repo.tags:
            commit_name = tag.commit.message.strip()
            tree['tags'][tag.name] = {
                'target': commit_name,
                'id': tag.name
            }

        while len(commits) > 0:
            cur_commit = commits.pop()
            if cur_commit not in visited:
                for parent in cur_commit.parents:
                    commits.add(parent)
            visited.add(cur_commit)

        while len(visited) > 0:
            cur_commit = visited.pop()
            commit_name = cur_commit.message.strip()
            tree['commits'][commit_name] = {
                'parents': [parent.message.strip() for parent in cur_commit.parents],
                'id': commit_name
            }

        if repo.head.is_detached:
            target = repo.commit('HEAD').message.strip()
        else:
            target = repo.head.ref.name

        tree['HEAD'] = {
            'target': target,
            'id': 'HEAD'
        }

        return tree

    def get_challenge(self):
        with open(self.level_path) as level_file:
            current_level, current_challenge = level_file.read().split()
        return current_level, current_challenge

    def write_challenge(self, level, challenge):
        with open(self.level_path, 'w+') as level_file:
            level_file.write(' '.join([level, challenge]))

    def get_last_commit(self):
        with open(self.last_commit_path) as last_commit_file:
            return last_commit_file.read()

    def write_last_commit(self, name):
        with open(self.last_commit_path, 'w+') as last_commit_file:
            last_commit_file.write(name)


def get_operator():
    cwd = os.getcwd().split(os.path.sep)

    for i in reversed(range(len(cwd))):
        path = os.path.sep.join(cwd[:i+1])
        gg_path = os.path.sep.join(cwd[:i+1] + ['.git', 'gud'])
        if os.path.isdir(gg_path):
            operator = Operator(path)
            operator.initialize()
            return operator
    return None


def get_topology(tree):
    tree['topology'] = None
    raise NotImplementedError


def parse_spec(file_name):
    # The purpose of this method is to get a more computer-readable commit tree
    with open(file_name) as spec_file:
        spec = spec_file.read()

    commits = []  # List of (commit_name, [parents], [branches], [tags])
    all_branches = set()
    all_tags = set()

    for line in spec.split('\n'):
        if len(line) == 0 or line[0] == '#':
            # Last line or comment
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
        level['topology'].append(commit_name)
        level['commits'][commit_name] = {
            'parents': parents,
            'id': commit_name
        }

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
