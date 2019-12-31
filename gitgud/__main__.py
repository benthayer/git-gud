import os
import sys
import subprocess

import argparse

from git import Repo
from git.exc import InvalidGitRepositoryError

from gitgud.operations import get_operator
from gitgud.operations import Operator
from gitgud.levels import all_levels
from gitgud.hooks import all_hooks

# TODO Add test suite so testing can be separate from main code


def show_tree():
    subprocess.call(["git", "log", "--graph", "--oneline", "--all"])


class InitializationError(Exception):
    pass


class GitGud:
    def __init__(self):
        self.file_operator = get_operator()  # Only gets operator if in a valid gitgud repo

        self.parser = argparse.ArgumentParser(prog='git gud')

        self.subparsers = self.parser.add_subparsers(title='Subcommands', metavar='<command>', dest='command')

        # TODO Add git gud help <command>, which would return the same output as git gud <command> -- help

        # TODO Display help message for subcommand when it fails.
        # ie `git gud load level1 challenge1 random-input` should have output similar to `git gud load --help`
        
        # Use "git gud help" to print helps of all subcommands.
        # "git gud help <command>" prints the description of the <command> but not help.
        # TODO Add longer descriptions

        help_parser = self.subparsers.add_parser('help', help='Show help for commands', description='Show help for commands') 
        start_parser = self.subparsers.add_parser('start', help='Git started!', description='Git started!')
        status_parser = self.subparsers.add_parser('status', help='Print out the current level', description='Print out the current level')
        instructions_parser = self.subparsers.add_parser('instructions', help='Show the instructions for the current level', description='Show the instructions for the current level')
        reset_parser = self.subparsers.add_parser('reset', help='Reset the current level', description='Reset the current level')
        reload_parser = self.subparsers.add_parser('reload', help='Reset the current level. Reload command is an alias for reset command.', description='Reset the current level. Reload command is an alias for reset command.')
        test_parser = self.subparsers.add_parser('test', help='Test to see if you\'ve successfully completed the current level', description='Test to see if you\'ve successfully completed the current level')
        progress_parser = self.subparsers.add_parser('progress', help='Continue to the next level', description='Continue to the next level')
        levels_parser = self.subparsers.add_parser('levels', help='List levels', description='List levels')
        challenges_parser = self.subparsers.add_parser('challenges', help='List challenges in current level or in other level if specified', description='List challenges in current level or in other level if specified')
        load_parser = self.subparsers.add_parser('load', help='Load a specific level or challenge', description='Load a specific level or challenge')
        commit_parser = self.subparsers.add_parser('commit', help='Quickly create and commit a file', description='Quickly create and commit a file')
        goal_parser = self.subparsers.add_parser('goal', help='Show a description of the current goal', description='Show a description of the current goal')
        show_tree_parser = self.subparsers.add_parser('show-tree', help='Show the current state of the branching tree', description='Show the current state of the branching tree')

        help_parser.add_argument('command_name', metavar='<command>', nargs='?')

        start_parser.add_argument('--force', action='store_true')

        challenges_parser.add_argument('level_name', metavar='level', nargs='?')

        load_parser.add_argument('level_name', metavar='level', help='Level to load')
        load_parser.add_argument('challenge_name', metavar='challenge', nargs='?', help='Challenge to load')

        commit_parser.add_argument('file', nargs='?')

        self.command_dict = {
            'help': self.handle_help,
            'start': self.handle_start,
            'status': self.handle_status,
            'instructions': self.handle_instructions,
            'reset': self.handle_reset,
            'reload': self.handle_reset,
            'test': self.handle_test,
            'progress': self.handle_progress,
            'levels': self.handle_levels,
            'challenges': self.handle_challenges,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'goal': self.handle_goal,
            'show-tree': self.handle_show_tree,
        }

    def is_initialized(self):
        return self.file_operator is not None

    def assert_initialized(self):
        if not self.is_initialized():
            raise InitializationError("Git gud not initialized. Use \"git gud start\" to initialize")

    def load_challenge(self, challenge):
        challenge.setup(self.file_operator)
        self.file_operator.write_challenge(challenge)
        show_tree()

    def handle_help(self, args):
        if args.command_name is None:
            self.parser.print_help()
        else:
            try:
                self.subparsers.choices[args.command_name].print_help()
            except KeyError:
                print('No such command exists: \"{}\"\n'.format(args.command_name))
                self.parser.print_help()

    def handle_start(self, args):
        # Make sure it's safe to initialize
        if not args.force:
            # We aren't forcing
            if self.file_operator:
                print('Repo {} already initialized for git gud.'.format(self.file_operator.path))
                print('Use --force to initialize {}.'.format(os.getcwd()))
                return

            self.file_operator = Operator(os.getcwd(), initialize_repo=False)

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
        try:
            self.file_operator.repo = Repo(self.file_operator.path)
        except InvalidGitRepositoryError:
            self.file_operator.repo = Repo.init(self.file_operator.path)

        if not os.path.exists(self.file_operator.gg_path):
            os.mkdir(self.file_operator.gg_path)
        with open(self.file_operator.last_commit_path, 'w+') as commit_file:
            commit_file.write('0')  # First commit will be 1
        with open(self.file_operator.level_path, 'w+') as level_file:
            level1 = next(iter(all_levels.values()))
            challenge1 = next(iter(level1.challenges.values()))
            level_file.write(challenge1.full_name())

        python_exec = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

        for git_hook_name, module_hook_name in all_hooks:
            path = os.path.join(self.file_operator.hooks_path, git_hook_name)
            with open(path, 'w+') as hook_file:
                hook_file.write('#!/bin/sh' + os.linesep)
                hook_file.write('' + python_exec + ' -m gitgud.hooks.' + module_hook_name + " $@" + os.linesep)
                hook_file.write(
                    "if [[ $? -ne 0 ]]" + os.linesep + "" \
                    "then" + os.linesep + "" \
                    "\t exit 1" + os.linesep+ "" \
                    "fi" + os.linesep)

            # Make the files executable

            mode = os.stat(path).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(path, mode)

        print('Git Gud successfully setup in {}'.format(os.getcwd()))

        self.file_operator.get_challenge().setup(self.file_operator)
        show_tree()

    def handle_status(self, args):
        if self.is_initialized():
            challenge_name = self.file_operator.get_challenge().full_name()
            print("Currently on challenge: \"{}\"".format(challenge_name))
        else:
            print("Git gud not initialized.")
            print("Initialize using \"git gud start\"")

    def handle_instructions(self, args):
        self.assert_initialized()
        self.file_operator.get_challenge().instructions()

    def handle_reset(self, args):
        self.assert_initialized()

        challenge = self.file_operator.get_challenge()
        print("Resetting...")
        challenge.setup(self.file_operator)
        show_tree()

    def handle_test(self, args):
        self.assert_initialized()
        challenge = self.file_operator.get_challenge()

        if challenge.test(self.file_operator):
            print("Challenge complete! `git gud progress` to advance to the next level")
        else:
            print("Challenge not complete, keep trying. `git gud reset` to start from scratch.")

    def handle_progress(self, args):
        self.assert_initialized()

        print("Progressing to next level...")

        challenge = self.file_operator.get_challenge()

        next_challenge = challenge.next_challenge
        if next_challenge is not None:
            self.load_challenge(next_challenge)
        else:
            print("Wow! You've complete every challenge, congratulations!")
            print("If you want to keep learning git, why not try contributing to git-gud by forking us at https://github.com/bthayer2365/git-gud/")
            print("We're always looking for contributions and are more than happy to accept both pull requests and suggestions!")

    def handle_levels(self, args):
        cur_level = self.file_operator.get_challenge().level

        print("Currently on level: \"{}\"\n".format(cur_level.name))
        
        for level in all_levels.values():
            # TODO Add description
            # 10 characters for the short IDs. 
            print("Level {:<10} :{:>2} challenge{}".format("\"" + level.name + "\"", len(level.challenges), ("", "s")[len(level.challenges) > 1]))
            for index, challenge in enumerate(level.challenges.values()):
                # " " * (characters allocated for ID - 6)
                print("{}Challenge {:>2} : {:<10}".format(" " * 4, index + 1, challenge.name))

    def handle_challenges(self, args):
        key_error_flag = False
        if args.level_name is None:
            level = self.file_operator.get_challenge().level
        else:
            try:
                level = all_levels[args.level_name]
            except KeyError:
                print("There is no level \"{}\".".format(args.level_name))
                print("You may run \"git gud levels\" to print all the levels. \n")
                level = self.file_operator.get_challenge().level
                key_error_flag = True
        
        if key_error_flag == True or args.level_name is None:
            print("Challenges in the current level \"{}\" : \n".format(level.name))
        else:
            print("Challenges for level \"{}\" : \n".format(level.name))

        for index, challenge in enumerate(level.challenges.values()):
            print(str(index + 1) + ": " + challenge.name)

    def handle_load(self, args):
        self.assert_initialized()
        if args.level_name in all_levels:
            level = all_levels[args.level_name]

            if args.challenge_name is not None:
                if args.challenge_name in all_levels[args.level_name].challenges:
                    challenge = level.challenges[args.challenge_name]
                    self.load_challenge(challenge)
                else:
                    print("Challenge \"{}\" does not exist".format(args.challenge_name))
                    print("To view challenges/levels, use git gud challenges or git gud levels")
            else:
                challenge = next(iter(level.challenges.values()))
                self.load_challenge(challenge)
        else:
            print("Level \"{}\" does not exist".format(args.level_name))
            print("To view challenges/levels, use git gud challenges or git gud levels")

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

        print("Simulating: Create file \"{}\"".format(commit_name))
        print("Simulating: git add {}".format(commit_name))
        print("Simulating: git commit -m \"{}\"".format(commit_name))

        self.file_operator.add_and_commit(commit_name)

        # Check if the newest commit is greater than the last_commit, if yes, then write

        if int(commit_name) > int(last_commit):
            self.file_operator.write_last_commit(commit_name)

    def handle_goal(self, args):
        self.assert_initialized()
        raise NotImplementedError

    def handle_show_tree(self, args):
        show_tree()

    def parse(self):
        args, _ = self.parser.parse_known_args()
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
