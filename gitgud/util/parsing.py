from copy import deepcopy


def parse_spec(spec_path):
    # The purpose of this method is to get a more computer-readable commit tree
    spec = spec_path.read_text()

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

        # There should never be more than one change or a space in a name
        assert ' ' not in commit_name

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
    # Used with test spec files
    # return json object representing the current commits

    level = {
        'topology': [],
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    for commit_name, parents, branches_here, tags_here in commits:
        level['topology'].append(commit_name)
        level['commits'][commit_name] = {
            'parents': parents,
            'id': commit_name
        }

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


def has_all_branches(skill, test):
    # Has all the other specified branches
    for branch_name in test['branches']:
        if branch_name not in skill['branches']:
            return False
    return True


def all_branches_correct(skill, test):
    for branch_name in test['branches']:
        if skill['branches'][branch_name]['target'] != \
                test['branches'][branch_name]['target']:
            return False
    return True


def has_no_extra_branches(skill, test):
    for branch_name in skill['branches']:
        if branch_name not in test['branches']:
            return False
    return True


def head_correct(skill, test):
    if skill['HEAD']['target'] != test['HEAD']['target']:
        return False
    return True


def has_all_tags(skill, test):
    # Has all tags specified
    for tag_name in test['tags']:
        if tag_name not in skill['tags']:
            return False
    return True


def all_tags_correct(skill, test):
    for tag_name in test['tags']:
        if skill['tags'][tag_name]['target'] != \
                test['tags'][tag_name]['target']:
            return False
    return True


def has_no_extra_tags(skill, test):
    for tag_name in skill['tags']:
        if tag_name not in test['tags']:
            return False
    return True


def check_commits(skill, test):
    for commit_name in test['commits']:
        if commit_name not in skill['commits']:
            return False

        skill_commit = skill['commits'][commit_name]
        test_commit = test['commits'][commit_name]

        # Commits must have the same number of parents and be in the same order
        if len(skill_commit['parents']) != len(test_commit['parents']):
            return False
        for skill_parent, test_parent in \
                zip(skill_commit['parents'], test_commit['parents']):
            if skill_parent != test_parent:
                return False
    return True


def tree_branches_to_lowercase(tree, branches):
    branch_dict = tree['branches']
    for branch in list(branch_dict.keys()):
        if branch in branches and not branch == branch.lower():
            branch_dict[branch.lower()] = branch_dict[branch]
            branch_dict[branch.lower()]['id'] = branch.lower()
            del branch_dict[branch]

    head = tree['HEAD']
    if head['target'] in branches:
        head['target'] = head['target'].lower()


def branches_to_lowercase(level_tree, setup_tree, test_tree):
    level_branches = set(level_tree['branches'].keys())
    setup_branches = set(setup_tree['branches'].keys())
    test_branches = set(test_tree['branches'].keys())
    added_branches = (level_branches | test_branches) - setup_branches

    tree_branches_to_lowercase(level_tree, added_branches)
    tree_branches_to_lowercase(test_tree, added_branches)


def name_from_map(level_tree, mapping):
    # Map other commits to themselves
    mapping = deepcopy(mapping)
    for commit_name in level_tree['commits']:
        if commit_name not in mapping:
            mapping[commit_name] = commit_name

    # Update references to merges in branches
    for branch in level_tree['branches']:
        level_tree['branches'][branch]['target'] = \
                mapping[level_tree['branches'][branch]['target']]

    # Update references to merges in tags
    for tag in level_tree['tags']:
        level_tree['tags'][tag]['target'] = \
                mapping[level_tree['tags'][tag]['target']]

    # Update HEAD if it points to a merge
    if level_tree['HEAD']['target'] in mapping:
        level_tree['HEAD']['target'] = mapping[level_tree['HEAD']['target']]

    new_commits = {}
    for commit_name, commit_info in level_tree['commits'].items():
        new_commits[mapping[commit_name]] = {
            'parents': [mapping[parent] for parent in commit_info['parents']],
            'id': mapping[commit_name]
        }

    level_tree['commits'] = new_commits


def get_non_merges(skill):
    non_merges = []
    for commit_name, commit_info in skill['commits'].items():
        if len(commit_info['parents']) <= 1:
            non_merges.append(commit_name)
    return non_merges


def name_merges(skill, test):
    # List merges.
    merges = {}  # (parent1, parent2, ...): "Name"
    for commit_name, commit_info in skill['commits'].items():
        if len(commit_info['parents']) >= 2:
            merges[tuple(commit_info['parents'])] = commit_name

    # This doesn't work if merges have other merges as parents
    # Use test to create a mapping for merges
    mapping = {}
    for commit_name, commit_info in test['commits'].items():
        if len(commit_info['parents']) >= 2:
            parents = tuple(commit_info['parents'])
            if parents in merges:
                merge_name = merges[parents]
                mapping[merge_name] = commit_name

    name_from_map(skill, mapping)


def test_ancestry(skill, test):
    # Tests that the graph of the git history matches

    if not check_commits(skill, test):
        return False

    if not has_all_branches(skill, test):
        return False
    if not all_branches_correct(skill, test):
        return False
    if not has_no_extra_branches(skill, test):
        return False

    if not has_all_tags(skill, test):
        return False
    if not all_tags_correct(skill, test):
        return False
    if not has_no_extra_tags(skill, test):
        return False

    if not head_correct(skill, test):
        return False

    return True
