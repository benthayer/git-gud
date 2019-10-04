from gitgud.operations import parse_tree
from gitgud.operations import level_json
from gitgud.operations import get_current_tree
from gitgud.operations import create_tree


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
        self.challenges = challenges
        pass


class BasicChallenge:
    def __init__(self, name):
        self.name = name
        self.path = f'{name}/'

    def setup(self):
        commits, head = parse_tree(self.path + 'setup.spec')
        create_tree(commits, head)

    def test(self):
        commits, head = parse_tree(self.path + 'test.spec')
        test_tree = level_json(commits, head)
        level_tree = get_current_tree()
        return test_level(level_tree, test_tree)