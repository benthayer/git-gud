from argparse import ArgumentParser


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
    checkout = commits[-1][0]
    del commits[-1]
    return commits, checkout


def main():
    with open('spec.spec') as spec_file:
        a = parse_tree(spec_file.read())
        print(a)
    pass


if __name__ == '__main__':
    main()
