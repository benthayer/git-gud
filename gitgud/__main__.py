import os
import sys

import argparse

from configparser import NoSectionError


from gitgud.operations import get_operator
from gitgud.operations import Operator
from gitgud.levels import all_levels

# TODO Add test suite so testing can be separate from main code


class InitializationError(Exception):
    pass


class GitGud:
    def __init__(self):
        self.file_operator = get_operator()  # Only gets operator if in a valid gitgud repo

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

        load_parser.add_argument('level', metavar='level_name', help='Level to load')
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
            raise InitializationError("Git gud not initialized. Use \"git gud start\" to initialize")

    def handle_start(self, args):
        # TODO Warn if there is already a git tree so we don't try to overwrite history

        if not args.force:
            # We aren't forcing
            if self.file_operator:
                print(f'Repo {self.file_operator.path} already initialized for git gud.')
                print(f'Use --force to initialize {os.getcwd()}.')
                return

            self.file_operator = Operator(os.getcwd())

            if os.path.exists(self.file_operator.git_path):
                # Current directory is a git repo
                print('Currently in a git repo. Use --force to force initialize here.')
                return
            if os.path.exists(self.file_operator.gg_path):
                # Current directory is a git repo
                print('Git gud has already initialized. Use --force to force initialize again.')
                return
            if len(os.listdir(self.file_operator.path)) != 0:
                print('Current directory is nonempty. Use --force to force initialize here.')
                return
        else:
            print('Force initializing git gud.')

        # After here, we initialize everything
        self.file_operator.initialize()

        python = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

        config_writer = self.file_operator.repo.config_writer()
        try:
            config_writer.remove_option('alias', 'gud')
        except NoSectionError:
            pass
        config_writer.add_value('alias', 'gud', f'"! {python} -m gitgud"')

        if not os.path.exists(self.file_operator.gg_path):
            os.mkdir(self.file_operator.gg_path)
        with open(self.file_operator.last_commit_path, 'w+') as commit_file:
            commit_file.write('0')  # First commit will be 1
        with open(self.file_operator.level_path, 'w+') as level_file:
            level_file.write('intro commits')

    def handle_progress(self, args):
        self.assert_initialized()

        challenge = self.file_operator.get_challenge()

        next_challenge = challenge.next_challenge
        if next_challenge is not None:
            next_challenge.setup(self.file_operator)
        else:
            print("Wow! You've complete every challenge, congratulations!")
            print("If you want to keep learning git, why not try contributing to git-gud by forking us at https://github.com/bthayer2365/git-gud/")
            print("We're always looking for a contributions and are more than happy to suggest both pull requests and suggestions!")

        self.file_operator.write_challenge(challenge)


    def handle_reset(self, args):
        self.assert_initialized()

        self.file_operator.get_challenge().setup(self.file_operator)

    def handle_levels(self, args):
        for level in all_levels:
            # TODO Make pretty
            # TODO Add description
            print(level.name)

    def handle_challenges(self, args):
        if args.level_name is None:
            level = self.file_operator.get_challenge().level
        else:
            level = all_levels[args.level_name]

        for challenge in level.challenges:
            print(challenge.name)

    def handle_load(self, args):
        self.assert_initialized()

        level = all_levels[args.level_name]
        try:
            level.challenges[args.challenge].setup(self.file_operator)
        except KeyError:
            first_level = next(iter(level.challenges.values()))
            first_level.setup(self.file_operator)

    def handle_commit(self, args):
        self.assert_initialized()

        last_commit = self.file_operator.get_last_commit()
        commit_name = str(int(last_commit) + 1)

        if args.file is not None:
            try:
                int(args.file)
                commit_name = args.file
            except ValueError:
                pass

        self.file_operator.add_and_commit(commit_name)

        # Check if the newest commit is greater than the last_commit, if yes, then write

        if int(commit_name) > int(last_commit):
            self.file_operator.write_last_commit(commit_name)

    def handle_instructions(self, args):
        self.assert_initialized()
        self.file_operator.get_challenge().instructions()

    def handle_goal(self, args):
        self.assert_initialized()
        raise NotImplementedError

    def handle_test(self, args):
        self.assert_initialized()
        challenge = self.file_operator.get_challenge()

        if challenge.test(self.file_operator):
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
