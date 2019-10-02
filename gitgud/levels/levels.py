from gitgud.operations import create_tree


def get_current_tree():
    # Return a json object with the same structure as in level_json

    tree = {
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    #

    raise NotImplementedError

    return tree

def get_topology(tree):
    tree['topology'] = None
    raise NotImplementedError

def parse_tree(tree_spec_file_name):
    # The purpose of this method is to get a more computer-readable commit tree
    with open(tree_spec_file_name) as tree_spec_file:
        tree_str = tree_spec_file.read()

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

class Sequence:
    def __init__(self, name):
        pass

class BasicLevel:
    def __init__(self, name):
        self.name = name
        self.path = 'name/'
    def setup(self):
        commits, head = parse_tree(self.path + 'setup.spec')
        create_tree(commits, head)
    def test(self):
        commits, head = parse_tree(self.path + 'test.spec')
        test_tree = level_json(commits, head)
        level_tree = get_current_tree()

        # Load working tree as json
        # Load test spec as json
        # Compare the two
        test_level()
        pass

