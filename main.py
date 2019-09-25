from argparse import ArgumentParser

from git import Repo


def parse_tree(tree_str):
    # The purpose of this method is to get a more computer-readable commit tree

    commits = []  # List of  (change, [parents], [branches], [tags])
    for line in tree_str.split('\n'):
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
            change = commit_str
        else:
            # Find parent
            change, parent = commit_str.split(':')
            change = change.strip()
            parent = parent.strip()

            parents = parent.split(' ')

        # We should have parents now

        assert ' ' not in change  # There should never be more than one change

        # Process ref_str
        refs = ref_str.split(',')
        branches = []
        tags = []
        for ref in refs:
            if ref[:4] == 'tag:':
                tags.append(ref[4:])
            else:
                branches.append(ref)
        commits.append((change, parents, branches, tags))

    head = commits[-1][0]

    del commits[-1]

    level = {
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    all_branches = []
    all_tags = []
    for name, parents, branches_here, tags_here in commits:
        level['commits'][name] = {
            'parents': parents,
            'id': name
        }
        if not parents:
            level['commits'][name]['rootCommit'] = True
        all_branches.extend(branches_here)
        all_tags.extend(tags_here)

    for branch, target in branches:
        level['branches'][branch] = {
            'target': target,
            'id': branch
        }

    for tag, target in tags:
        level['tags'][tag] = {
            'target': branch,
            'id': tag
        }

    level['HEAD'] = {
        'target': head,
        'id': 'HEAD'
    }

    return commits, head


def main():
    with open('spec.spec') as spec_file:
        a = parse_tree(spec_file.read())
        print(a)
    pass


if __name__ == '__main__':
    main()
