import os
import sys

import argparse

from git import Repo
from git.exc import NoSuchPathError

from gitgud.operations import FileOperator
from gitgud.levels import all_levels

# TODO Add test suite so testing can be separate from main code


class InitializationError(Exception):
    pass


class GitGud:
    def __init__(self):
        self.path = os.getcwd()

        self.file_operator = None

        self.parser = argparse.ArgumentParser(prog='git gud')

        subparsers = self.parser.add_subparsers(title='Subcommands', metavar='<command>', dest='command')

        # TODO Add git gud help <command>, which would return the same output as git gud <command> -- help

        # TODO Display help message for subcommand when it fails.
        # ie `git gud load level1 challenge1 random-input` should have output similar to `git gud load --help`

        start_parser = subparsers.add_parser('start', help='Git started!')
        progress_parser = subparsers.add_parser('progress', help='Continue to the next level')
        reset_parser = subparsers.add_parser('reset', help='Reset the current level')
        levels_parser = subparsers.add_parser('levels', help='List levels')
        challenges_parser = subparsers.add_parser('challenges', help='List challenges in current level or in other level if specified')
        load_parser = subparsers.add_parser('load', help='Load a specific level or challenge')
        commit_parser = subparsers.add_parser('commit', help='Quickly create and commit a file')
        instructions_parser = subparsers.add_parser('instructions', help='Show the instructions for the current level')
        goal_parser = subparsers.add_parser('goal', help='Show a description of the current goal')
        test_parser = subparsers.add_parser('test', help='Test to see if you\'ve successfully completed the current level')
        show_tree_parser = subparsers.add_parser('show-tree', help='Show the current state of the branching tree')

        start_parser.add_argument('--force', action='store_true')

        challenges_parser.add_argument('level', nargs='?')

        load_parser.add_argument('level', help='Level to load')
        load_parser.add_argument('challenge', nargs='?', help='Challenge to load')

        commit_parser.add_argument('file', nargs='?')

        self.command_dict = {
            'start': self.handle_start,
            'progress': self.handle_progress,
            'reset': self.handle_reset,
            'levels': self.handle_levels,
            'challenges': self.handle_challenges,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'instructions': self.handle_instructions,
            'goal': self.handle_goal,
            'test': self.handle_test,
            'show_tree': self.handle_show_tree,
        }

    def assert_initialized(self):
        if not self.file_operator:
            raise InitializationError()

    def handle_start(self, args):
        # TODO Warn if there is already a git tree so we don't try to overwrite history

        if not args.force:
            # We aren't forcing
            if os.path.exists(self.git_path):
                # Current directory is a git repo
                print('Currently in a git repo. Use --force to force initialize here.')
                return
            if os.path.exists(self.gg_path):
                # Current directory is a git repo
                print('Git gud has already initialized. Use --force to force initialize again.')
                return
            if len(os.listdir(self.path)) != 0:
                print('Current directory is nonempty. Use --force to force initialize here.')
                return
        else:
            print('Force initializing git gud.')

        # After here, we initialize everything
        try:
            repo = Repo(self.path)
        except NoSuchPathError:
            repo = Repo.init(self.path)

        python = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

        config_writer = repo.config_writer()
        config_writer.remove_option('alias', 'gud')
        config_writer.add_value('alias', 'gud', f'"! {python} -m gitgud"')

        if not os.path.exists(self.gg_path):
            os.mkdir(self.gg_path)
        with open(self.last_commit_path, 'w+') as commit_file:
            commit_file.write('0')  # First commit will be 1
        with open(self.level_path, 'w+') as level_file:
            level_file.write('intro commits')

    def handle_progress(self, args):
        self.
        with open(self.level_path) as level_file:
            current_level, current_challenge = level_file.read().split()

        all_levels[current_level].challenges[current_challenge].next_level.setup()

    def handle_reset(self, args):
        with open(self.level_path) as level_file:
            current_level, current_challenge = level_file.read().split()

        all_levels[current_level].challenges[current_challenge].setup()

    def handle_levels(self, args):
        for level in all_levels:
            # TODO Make pretty
            # TODO Add description
            print(level.name)

    def handle_challenges(self, args):
        with open(self.level_path) as level_file:
            current_level, current_challenge = level_file.read().split()

        try:
            current_level = args.level
        except NameError:
            pass

        for challenge in all_levels[current_level].challenges:
            # TODO Make pretty
            # TODO Add description
            print(challenge.name)

    def handle_load(self, args):
        # git gud load level
        # git gud load level challenge

        level = all_levels[args.level]
        try:
            level.challenges[args.challenge].setup()
        except KeyError:
            first_level = next(iter(level.challenges.values()))
            first_level.setup()

    def handle_commit(self, args):
        if os.path.exists(self.last_commit_path):
            with open(self.last_commit_path) as last_commit_file:
                last_commit = last_commit_file.read()
        else:
            last_commit = '1'

        try:
            commit_name = args.file
        except AttributeError:
            commit_name = str(int(last_commit) + 1)

        should_write = False
        try:
            if int(args.file) > int(last_commit):
                should_write = True
        except ValueError:
            # args.file is not a number
            pass

        if should_write:
            with open(self.last_commit_path, 'w+') as last_commit_file:
                last_commit_file.write(commit_name)

        return add_and_commit(commit_name)

    def handle_instructions(self, args):
        raise NotImplementedError

    def handle_goal(self, args):
        raise NotImplementedError

    def handle_test(self, args):
        with open(self.level_path) as level_file:
            level, challenge = level_file.read().split()
        if all_levels[level].challenges[challenge].test():
            print("Level complete! `git gud progress` to advance to the next level")
        else:
            print("Level not complete, keep trying. `git gud reset` to start from scratch.")

    def handle_show_tree(self, args):
        raise NotImplementedError

    def parse(self):
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            try:
                self.command_dict[args.command](args)
            except InitializationError:
                print("Git gud has not been initialized. Initialize using \"git gud start\"")
                pass


if __name__ == '__main__':
    GitGud().parse()
