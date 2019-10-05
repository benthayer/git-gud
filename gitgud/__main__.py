import os

import argparse

from gitgud.operations import add_and_commit
from git import Repo

# TODO Add test suite so testing can be separate from main code

class GitGud:
    def __init__(self):
        self.path = os.getcwd()
        self.git_path = os.path.join(self.path, '.git')
        self.gg_path = os.path.join(self.git_path, 'gud')

        self.parser = argparse.ArgumentParser(prog='git gud')

        subparsers = self.parser.add_subparsers(title='Subcommands', metavar='<command>', dest='command')

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

        self.command_dict = {
            'start': self.handle_start,
            'progress': self.handle_progress,
            'levels': self.handle_levels,
            'challenges': self.handle_challenges,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'instructions': self.handle_instructions,
            'goal': self.handle_goal,
            'test': self.handle_test,
            'show_tree': self.handle_show_tree,
        }

    def handle_start(self, args):
        # TODO Warn if there is already a git tree so we don't try to overwrite history
        # TODO Use path separators to join paths
        # TODO Be smarter about where I'm getting paths in general

        # TODO Add alias so command can be run as `git gud`

        repo = Repo('')
        git_exec = repo.GitCommandWrapperType()
        git_exec.execute(['config', 'alias.gud', '"! python -m gitgud"'])

        gg_folder = '.git/gud/'
        commit_file_name = 'tree/.git/gud/last_commit'
        level_file_name = 'tree/.git/gud/level'
        if not os.path.exists(gg_folder):
            os.mkdir(gg_folder)
        with open(commit_file_name, 'w+') as commit_file:
            commit_file.write('0')  # First commit will be 1
        with open(level_file_name, 'w+') as level_file:
            level_file.write('welcome')  # TODO Add welcome level that gives instructions for git gud

    def handle_progress(self, args):
        pass

    def handle_levels(self, args):
        pass

    def handle_challenges(self, args):
        pass

    def handle_load(self, args):
        # git gud load level1
        # git gud load challenge1
        # git gud load level1 challenge1
        pass

    def handle_commit(self, args):
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

    def handle_instructions(self, args):
        pass

    def handle_goal(self, args):
        pass

    def handle_test(self, args):
        pass

    def handle_show_tree(self, args):
        pass

    def parse(self):
        args = self.parser.parse_args()
        self.command_dict[args.command](args)


if __name__ == '__main__':
    GitGud().parse()
