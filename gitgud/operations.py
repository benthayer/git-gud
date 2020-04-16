import os
import shutil
import datetime as dt
import email.utils
import json

from glob import glob

from git import Repo

from gitgud import actor
from gitgud import actor_string
from gitgud.skills import all_skills


class Operator:
    def __init__(self, path, initialize_repo=True):
        self.path = path
        if initialize_repo:
            self.repo = Repo(os.getcwd())
        else:
            self.repo = None

        self.git_path = os.path.join(self.path, '.git')
        self.hooks_path = os.path.join(self.git_path, 'hooks')
        self.gg_path = os.path.join(self.git_path, 'gud')
        self.last_commit_path = os.path.join(self.gg_path, 'last_commit.txt')
        self.commits_json_path = os.path.join(self.gg_path, 'commits.csv')
        self.level_path = os.path.join(self.gg_path, 'current_level.txt')

    def add_file_to_index(self, filename):
        open('{}/{}'.format(self.path, filename), 'w+').close()
        self.repo.index.add([filename])

    def add_and_commit(self, name):
        # TODO Commits with the same time have arbitrary order when using git log, set time of commit to fix
        self.add_file_to_index(name)
        commit = self.repo.index.commit(name, author=actor, committer=actor, skip_hooks=True)

        return commit
    
    def clear_tree_and_index(self):
        dirs = []
        for x in [('**', '.*'), ('**',)]:
            path_spec = os.path.join(self.path, *x)
            for path in glob(path_spec, recursive=True):
                if not os.path.sep + '.git' + os.path.sep in path:
                    if os.path.isfile(path):
                        os.unlink(path)
                    else:
                        dirs.append(path)

        # TODO GitPython set index to working tree
        self.repo.git.add(update=True)
        # TODO GitPython clear index (for initial commits)
        self.repo.index.commit("Clearing index", skip_hooks=True)  # Easiest way to clear the index is to commit an empty directory

        dirs.remove(self.path + os.path.sep)  # Don't remove current directory

        for path in os.listdir(self.path):
            if path != '.git':
                shutil.rmtree(path)

    def create_tree(self, commits, head):
        branches = self.repo.branches
        try:
            # TODO GitPython detach head
            self.repo.git.checkout(self.repo.head.commit)  # Detached head, we can now delete everything
        except ValueError:
            pass
        self.clear_tree_and_index()

        for branch in branches:
            self.repo.delete_head(branch, force=True)
        self.repo.delete_tag(*self.repo.tags)

        commit_objects = {}
        counter = len(commits)
        for name, parents, branches, tags in commits:
            committime = dt.datetime.now(dt.timezone.utc).astimezone().replace(microsecond=0)
            committime_offset = dt.timedelta(seconds=counter) + committime.utcoffset()
            committime_rfc = email.utils.format_datetime(committime - committime_offset)
            # commit = (name, parents, branches, tags)
            parents = [commit_objects[parent] for parent in parents]
            if parents:
                # TODO GitPython detach head
                self.repo.git.checkout(parents[0])
            if len(parents) < 2:
                # Not a merge
                self.add_file_to_index(name)
                commit_obj = self.repo.index.commit(name, author=actor, committer=actor, author_date=committime_rfc, commit_date=committime_rfc, parent_commits=parents, skip_hooks=True)
            else:
                assert name[0] == 'M'
                int(name[1:])  # Fails if not a number

                # To handle octopus merges, we merge each branch into the index one by one, then commit
                for parent in parents[1:]:
                    merge_base = self.repo.merge_base(parents[0], parent)
                    self.repo.index.merge_tree(parent, base=merge_base)
                commit_obj = self.repo.index.commit(name, author=actor, committer=actor, author_date=committime_rfc, commit_date=committime_rfc, parent_commits=parents, skip_hooks=True)

            commit_objects[name] = commit_obj

            for branch in branches:
                self.repo.create_head(branch, self.repo.head.commit)

            for tag in tags:
                self.repo.create_tag(tag, self.repo.head.commit)
            # TODO Log commit hash and info
            counter = counter - 1

        # TODO Checkout using name
        head_is_commit = True
        for branch in self.repo.branches:
            if branch.name == head:
                branch.checkout()
                head_is_commit = False

        if head_is_commit:
            self.repo.git.checkout(commit_objects[head])

    # Parses commit msg for keywords (e.g. Revert)
    @staticmethod
    def parse_name(commit_msg):
        if "Revert" in commit_msg:
            commit_msg = commit_msg[8:-64]
            commit_msg += '-'
        return commit_msg

    def get_current_tree(self):
        # Return a json object with the same structure as in level_json

        repo = self.repo

        tree = {
            'branches': {},  # 'branch_name': {'target': 'commit_id', 'id': 'branch_name'}
            'tags': {},  # 'tag_name': {'target': 'commit_id', 'id': 'tag_name'}
            'commits': {},  # '2': {'parents': ['1'], 'id': '1'}
            'HEAD': {}  # 'target': 'branch_name', 'id': 'HEAD'
        }

        commits = set()
        visited = set()

        for branch in repo.branches:
            commits.add(branch.commit)
            commit_name = branch.commit.message.strip()
            commit_name = self.parse_name(commit_name)
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
            # If revert detected, modifies commit_name; o/w nothing happens
            commit_name = self.parse_name(commit_name)

            tree['commits'][commit_name] = {
                'parents': [self.parse_name(parent.message.strip()) for parent in cur_commit.parents],
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

    def read_level_file(self):
        with open(self.level_path) as level_file:
            return level_file.read()

    def get_level(self):
        skill_name, level_name = self.read_level_file().split()
        return all_skills[skill_name][level_name]

    def write_level(self, level):
        with open(self.level_path, 'w+') as skill_file:
            skill_file.write(' '.join([level.skill.name, level.name]))

    def get_last_commit(self):
        with open(self.last_commit_path) as last_commit_file:
            return last_commit_file.read()

    def write_last_commit(self, name):
        with open(self.last_commit_path, 'w+') as last_commit_file:
            last_commit_file.write(name)

    def clear_tracked_commits(self):
        with open(self.commits_json_path, 'w'):
            pass

    def track_commit(self, first_hash, second_hash, action):
        # Used to track rebases, amends and reverts
        with open(self.commits_json_path, 'a') as commit_tracker_file:
            commit_tracker_file.write(','.join([first_hash, second_hash, action]))
            commit_tracker_file.write('\n')


def get_operator():
    cwd = os.getcwd().split(os.path.sep)

    for i in reversed(range(len(cwd))):
        path = os.path.sep.join(cwd[:i+1])
        gg_path = os.path.sep.join(cwd[:i+1] + ['.git', 'gud'])
        if os.path.isdir(gg_path):
            return Operator(path)
    return None
