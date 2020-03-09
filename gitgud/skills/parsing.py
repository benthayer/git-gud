from importlib_resources import files

import os

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


def test_skill(skill, test):
    # We don't know the names of merges, so we match them with their test names
    # TODO Only works when merges don't have other merges as parents
    # TODO Topological sort merge commits
    skill = deepcopy(skill)
    merge_name_map = {}
    for commit_name in skill['commits']:
        skill_commit = skill['commits'][commit_name]
        if len(skill_commit['parents']) >= 2:  # TODO Stop here to get list of merges
            for test_commit_name in test['commits']:  # TODO Do this iteration in an intelligent manner
                test_commit = test['commits'][test_commit_name]
                parents_equal = True
                skill_parents = skill_commit['parents']
                test_parents = test_commit['parents']

                for skill_parent, test_parent in zip(skill_parents, test_parents):
                    if skill_parent != test_parent:
                        parents_equal = False
                        break
                if len(skill_parents) == len(test_parents) and parents_equal:
                    merge_name_map[test_commit_name] = commit_name

    # TODO Update parents to reference merge commits by new name

    # Check commits
    if len(test['commits']) != len(skill['commits']):
        return False
    for commit_name in test['commits']:
        test_commit = test['commits'][commit_name]
        if commit_name not in skill['commits']:
            if merge_name_map[commit_name] in skill['commits']:
                # It's a known merge
                skill_commit = skill['commits'][merge_name_map[commit_name]]
            else:
                return False
        else:
            skill_commit = skill['commits'][commit_name]

        # Commits must have the same number of parents and be in the same order
        if len(skill_commit['parents']) != len(test_commit['parents']):
            return False
        for skill_parent, test_parent in zip(skill_commit['parents'], test_commit['parents']):
            if skill_parent != test_parent:
                return False

    # Check branches
    if len(test['branches']) != len(skill['branches']):
        return False
    for branch_name in test['branches']:
        if branch_name not in skill['branches']:
            return False
        if skill['branches'][branch_name]['target'] != test['branches'][branch_name]['target']:
            if merge_name_map[test['branches'][branch_name]['target']] != skill['branches'][branch_name]['target']:
                return False  # It's also not a known merge

    # Check tags
    if len(test['tags']) != len(skill['tags']):
        return False
    for tag_name in test['tags']:
        if tag_name not in skill['tags']:
            return False
        if skill['tags'][tag_name]['target'] != test['tags'][tag_name]['target']:
            return False

    # Check HEAD
    if skill['HEAD']['target'] != test['HEAD']['target']:
        return False

    return True