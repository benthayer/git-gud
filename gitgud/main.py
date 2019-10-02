from argparse import ArgumentParser

import os

from gitgud.operations import add_and_commit

# TODO Add test suite so testing can be separate from main code


def handle_start():
    # TODO Use path separators to join paths
    # TODO Be smarter about where I'm getting paths in general

    # TODO Add alias so command can be run as `git gud`
    gg_folder = 'tree/.git/gud/'
    commit_file_name = 'tree/.git/gud/last_commit'
    level_file_name = 'tree/.git/gud/level'
    if not os.path.exists(gg_folder):
        os.mkdir(gg_folder)
    with open(commit_file_name, 'w+') as commit_file:
        commit_file.write('0')  # First commit will be 1
    with open(level_file_name, 'w+') as level_file:
        level_file.write('welcome')  # TODO Add welcome level that gives instructions for git gud


def handle_commit():
    file_path = 'tree/.git/gud/last_commit'

    if os.path.exists(file_path):
        with open('tree/.git/gud/last_commit') as last_commit_file:
            last_commit = last_commit_file.read()
    else:
        last_commit = '1'

    commit_name = str(int(last_commit) + 1)

    with open(file_path, 'w+') as last_commit_file:
        last_commit_file.write(commit_name)

    return add_and_commit(commit_name)


def handle_load(level_name):
    pass


def handle_instructions(level_name):
    pass


def handle_test(level_name):
    pass


def handle_save():

    pass


def main():
    parser = ArgumentParser(description="A tool for learning git concepts.")
    parser.add_argument('load', )
    parser.add_argument('instructions')
    parser.add_argument('test')
    args = parser.parse_args()
    # git gud load level1
    #
    handle_start()
    handle_load()
    handle_instructions()
    handle_test()

    pass


if __name__ == '__main__':
    main()
