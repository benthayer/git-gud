import os

import argparse

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


def handle_challenges(args):
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


def handle_show_tree(args):
    pass


def main():
    parser = argparse.ArgumentParser(prog='git gud')

    subparsers = parser.add_subparsers(title='Subcommands', metavar='<command>', dest='command')

    # TODO Add git gud help <command>, which would return the same output as git gud <command> -- help

    # TODO Display help message for subcommand when it fails.
    # ie `git gud load level1 challenge1 random-input` should have output similar to `git gud load --help`

    start_parser = subparsers.add_parser('start', help='Git started!')
    progress_parser = subparsers.add_parser('progress', help='Continue to the next level')
    levels_parser = subparsers.add_parser('levels', help='List levels')
    challenges_parser = subparsers.add_parser('challenges', help='List challenges in current level or in other level if specified')
    load_parser = subparsers.add_parser('load', help='Load a specific level or challenge')
    commit_parser = subparsers.add_parser('commit', help='Quickly create and commit a file')
    instructions_parser = subparsers.add_parser('instructions', help='Show the instructions for the current level')
    goal_parser = subparsers.add_parser('goal', help='Show a description of the current goal')
    test_parser = subparsers.add_parser('test', help='Test to see if you\'ve successfully completed the current level')
    show_tree_parser = subparsers.add_parser('show-tree', help='Show the current state of the branching tree')

    start_parser.add_argument('--force')

    challenges_parser.add_argument('level', nargs='?')

    load_parser.add_argument('level', help='Level to load')
    load_parser.add_argument('challenge', nargs='?', help='Challenge to load')

    commit_parser.add_argument('file', nargs='?')

    args = parser.parse_args()

    command_dict = {
        'start': handle_start,
        'progress': handle_progress,
        'levels': handle_levels,
        'challenges': handle_challenges,
        'load': handle_load,
        'commit': handle_commit,
        'instructions': handle_instructions,
        'goal': handle_goal,
        'test': handle_test,
        'show_tree': handle_show_tree,

    }

    command_dict[args.command](args)



if __name__ == '__main__':
    main()
