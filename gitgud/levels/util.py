import os

from collections import OrderedDict

from gitgud.operations import parse_spec
from gitgud.operations import level_json


def test_level(level, test):
    # Check commits
    if len(test['commits']) != len(level['commits']):
        return False
    for commit_name in test['commits']:
        if commit_name not in level['commits']:
            return False
        level_commit = level['commits'][commit_name]
        test_commit = test['commits'][commit_name]

        # Commits must have the same number of parents and be in the same order
        if len(level_commit['parents']) != len(test_commit['parents']):
            return False
        for level_parent, test_parent in zip(level_commit['parents'], test_commit['parents']):
            if level_parent != test_parent:
                return False

    # Check branches
    if len(test['branches']) != len(level['branches']):
        return False
    for branch_name in test['branches']:
        if branch_name not in level['branches']:
            return False
        if level['branches'][branch_name]['target'] != test['branches'][branch_name]['target']:
            return False

    # Check tags
    if len(test['tags']) != len(level['tags']):
        return False
    for tag_name in test['tags']:
        if tag_name not in level['tags']:
            return False
        if level['tags'][tag_name]['target'] != test['tags'][tag_name]['target']:
            return False

    # Check HEAD
    if level['HEAD']['target'] == test['HEAD']['target']:
        return False

    return True


class Level:
    def __init__(self, name, challenges):
        self.name = name
        self.challenges = OrderedDict()
        for challenge in challenges.values():
            self.challenges[challenge.name] = challenge


class Challenge:
    def __init__(self, name):
        self.name = name
        self.level_name = None

    def setup(self):
        pass

    def instructions(self):
        pass

    def test(self):
        pass


class BasicChallenge(Challenge):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

    def setup(self, file_operator):
        commits, head = parse_spec(os.path.join(self.path, 'setup.spec'))
        file_operator.create_tree(commits, head)

        latest_commit = '0'
        for commit_name, _, _, _ in commits:
            if int(commit_name) > int(latest_commit):
                latest_commit = commit_name

        file_operator.write_last_commit(latest_commit)

    def instructions(self):
        # TODO Go through instructions
        pass

    def test(self, file_operator):
        commits, head = parse_spec(os.path.join(self.path, 'test.spec'))
        test_tree = level_json(commits, head)
        level_tree = file_operator.get_current_tree()
        return test_level(level_tree, test_tree)