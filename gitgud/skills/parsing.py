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
    # Used with test spec files, return a json object to be compared with the tree of the level

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


def name_merges(skill, test):
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
    return merge_name_map


def has_all_branches(skill, test):
    # Has HEAD
    if test['HEAD']['target'] in skill['branches']:
        return False

    # Has all the other specified branches
    for branch_name in test['branches']:
        if branch_name not in skill['branches']:
            return False

    return True


def all_branches_correct(skill, test):
    for branch_name in test['branches']:
        if skill['branches'][branch_name]['target'] != test['branches'][branch_name]['target']:
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
        if skill['tags'][tag_name]['target'] != test['tags'][tag_name]['target']:
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
        for skill_parent, test_parent in zip(skill_commit['parents'], test_commit['parents']):
            if skill_parent != test_parent:
                return False
    return True


def test_ancestry(skill, test):
    # Tests that the graph of the git history matches 

    # skill = name_merges(skill, test)
    
    if not check_commits(skill, test):
        return False

    if not has_all_branches(skill, test):
        return False
    if not all_branches_correct(skill, test):
        return False
    if not has_all_tags(skill, test):
        return False
    if not all_tags_correct(skill, test):
        return False
    if not head_correct(skill, test):
        return False

    return True

