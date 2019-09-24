from argparse import ArgumentParser


def parse_tree(filename):
    # The purpose of this method is to get a more computer-readable commit tree
    #
    commits = []
    with open(filename) as f:
        for line in f:
            if '(' in line:
                commit_str = line[:line.find('(')]
                ref_str = line[line.find('('):]
            else:
                commit_str = line
                ref_str = ''
            if commit_str[0] is ':':
                # This is a merge commit
                parents = commit_str[1].split(' ')
            else:
                # This is a normal commit
                change = commit_str.strip()
                pass


    pass


def main():
    parser = ArgumentParser()
    parser.add_argument()


if __name__ == '__main__':
    main()
