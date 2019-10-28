import os

from copy import deepcopy


# TODO GitPython topology
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


def test_level(level, test):
    # We don't know the names of merges, so we match them with their test names
    # TODO Only works when merges don't have other merges as parents
    # TODO Topological sort merge commits
    level = deepcopy(level)
    merge_name_map = {}
    for commit_name in level['commits']:
        level_commit = level['commits'][commit_name]
        if len(level_commit['parents']) >= 2:  # TODO Stop here to get list of merges
            for test_commit_name in test['commits']:  # TODO Do this iteration in an intelligent manner
                test_commit = test['commits'][test_commit_name]
                parents_equal = True
                level_parents = level_commit['parents']
                test_parents = test_commit['parents']

                for level_parent, test_parent in zip(level_parents, test_parents):
                    if level_parent != test_parent:
                        parents_equal = False
                        break
                if len(level_parents) == len(test_parents) and parents_equal:
                    merge_name_map[test_commit_name] = commit_name

    # TODO Update parents to reference merge commits by new name

    # Check commits
    if len(test['commits']) != len(level['commits']):
        return False
    for commit_name in test['commits']:
        test_commit = test['commits'][commit_name]
        if commit_name not in level['commits']:
            if merge_name_map[commit_name] in level['commits']:
                # It's a known merge
                level_commit = level['commits'][merge_name_map[commit_name]]
            else:
                return False
        else:
            level_commit = level['commits'][commit_name]

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
            if merge_name_map[test['branches'][branch_name]['target']] != level['branches'][branch_name]['target']:
                return False  # It's also not a known merge

    # Check tags
    if len(test['tags']) != len(level['tags']):
        return False
    for tag_name in test['tags']:
        if tag_name not in level['tags']:
            return False
        if level['tags'][tag_name]['target'] != test['tags'][tag_name]['target']:
            return False

    # Check HEAD
    if level['HEAD']['target'] != test['HEAD']['target']:
        return False

    return True

class NamedList:
    # Pass in list of tuples in format (reference, Object), where reference is of type str
    def __init__(self, data=[]):
        self.namedict = {d[0]:i for i, d in enumerate(data)}
        self.items = [obj for name, obj in data]
    
    def __getitem__(self, query):
        if isinstance(query, int):
            return self.items[query]
        elif isinstance(query, str):
            return self.items[self.namedict[query]]
        else:
            return None
    def __iter__(self):
        return self.items.__iter__()
    def __len__(self):
        return len(self.items)
    def __setitem__(self, key, item):
        if isinstance(key, str):
            self.namedict[key] = len(self.items)
            self.items.append(item)
        else:
            raise TypeError
    
    def values(self):
        return self.items
    def keys(self):
        return self.namedict.keys()

class Level():
    def __init__(self, name, challenges):
        self.name = name
        self.challenges = NamedList()
        for challenge in challenges:
            challenge.level = self
            self.challenges[challenge.name] = challenge


class Challenge:
    def __init__(self, name):
        self.name = name
        self.level = None
        self.next_challenge = None

    def full_name(self):
        return '{} {}'.format(self.level.name, self.name)

    def setup(self, file_operator):
        pass

    def instructions(self):
        pass

    def test(self, file_operator):
        pass


class BasicChallenge(Challenge):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path
        self.setup_spec_path = os.path.join(self.path, 'setup.spec')
        self.instructions_path = os.path.join(self.path, 'instructions.txt')
        self.test_spec_path = os.path.join(self.path, 'test.spec')

    def setup(self, file_operator):
        print('Setting up challenge: "{}"'.format(self.full_name()))
        commits, head = parse_spec(self.setup_spec_path)
        file_operator.create_tree(commits, head)

        latest_commit = '0'
        for commit_name, _, _, _ in commits:
            if int(commit_name) > int(latest_commit):
                latest_commit = commit_name

        file_operator.write_last_commit(latest_commit)
        print("Setup complete")
        print("Type \"git gud instructions\" to view instructions")

    def instructions(self):
        print('Printing instructions for challenge: "{}"'.format(self.full_name()))
        with open(self.instructions_path) as instructions_file:
            for line in instructions_file:
                if line[:3] == '>>>':
                    input(">>>")
                else:
                    print(line.strip())

    def test(self, file_operator):
        print('Testing completion for challenge: "{}"'.format(self.full_name()))
        commits, head = parse_spec(self.test_spec_path)
        test_tree = level_json(commits, head)
        level_tree = file_operator.get_current_tree()
        return test_level(level_tree, test_tree)
