from argparse import ArgumentParser

from git import Repo


def parse_tree(tree_str):
    # The purpose of this method is to get a more computer-readable commit tree

    commits = []  # List of  (commit_name, [parents], [branches], [tags])
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
                tags.append(ref[4:])
            else:
                branches.append(ref)
        commits.append((commit_name, parents, branches, tags))

    head = commits[-1][0]

    del commits[-1]
    # We've formally replicated the input string in memory

    level = {
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    all_branches = []
    all_tags = []
    for commit_name, parents, branches_here, tags_here in commits:
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

    return level, commits, head


# TODO Commit
# TODO Test
# TODO Save
# TODO Load
# TODO Instructions
# TODO convert commit tree into spec format
# TODO convert spec format into commit tree

def main():
    with open('spec.spec') as spec_file:
        a = parse_tree(spec_file.read())
        print(a)
    pass


if __name__ == '__main__':
    main()
