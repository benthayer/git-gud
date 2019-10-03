import os
import sys

from gitgud.operations import add_and_commit

# TODO Add test suite so testing can be separate from main code


def handle_start(args):
    # TODO Warn if there is already a git tree so we don't try to overwrite history
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


def handle_progress(args):
    pass


def handle_levels(args):
    pass


def handle_load(args):
    # git gud load level1
    # git gud load challenge1
    # git gud load level1 challenge1
    pass


def handle_commit(args):
    # git gud commit
    # git gud commit A

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


def handle_instructions(args):
    pass


def handle_goal(args):
    pass


def handle_test(args):
    pass


def handle_save(args):
    pass


def default(args):
    pass


def main():
    args = sys.argv[1:]
    print(args)

    if args[1] == 'start':
        handler = handle_start
    elif args[1] == 'progress':
        handler = handle_progress
    elif args[1] == 'levels':
        handler = handle_levels
    elif args[1] == 'load':
        handler = handle_load
    elif args[1] == 'commit':
        handler = handle_commit
    elif args[1] == 'instructions':
        handler = handle_instructions
    elif args[1] == 'goal':
        handler = handle_goal
    elif args[1] == 'test':
        handler = handle_test
    elif args[1] == 'save':
        handler = handle_save
    else:
        handler = default

    handler(args[2:])


if __name__ == '__main__':
    main()
