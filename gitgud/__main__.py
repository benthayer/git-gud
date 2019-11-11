import os
import sys
import subprocess
import webbrowser

import argparse

from git import Repo
from git.exc import InvalidGitRepositoryError

from gitgud.operations import get_operator
from gitgud.operations import Operator
from gitgud.skills import all_skills
from gitgud.skills.util import print_all_complete
from gitgud.hooks import all_hooks

# TODO Add test suite so testing can be separate from main code


def show_tree():
    print("Simulating: git log --graph --oneline --all ")
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
        # ie `git gud load skill1 level1 random-input` should have output similar to `git gud load --help`
        
        # Use "git gud help" to print helps of all subcommands.
        # "git gud help <command>" prints the description of the <command> but not help.
        # TODO Add longer descriptions

        help_parser = self.subparsers.add_parser('help', help='Show help for commands', description='Show help for commands') 
        start_parser = self.subparsers.add_parser('start', help='Git started!', description='Git started!')
        status_parser = self.subparsers.add_parser('status', help='Print out the name of the current level', description='Print out the name of the current level')
        instructions_parser = self.subparsers.add_parser('instructions', help='Show the instructions for the current level', description='Show the instructions for the current level')
        goal_parser = self.subparsers.add_parser('goal', help='Concisely show what needs to be done to complete the level.', description='Concisely show what needs to be done to complete the level.')
        reset_parser = self.subparsers.add_parser('reset', help='Reset the current level', description='Reset the current level')
        reload_parser = self.subparsers.add_parser('reload', help='Reset the current level. Reload command is an alias for reset command.', description='Reset the current level. Reload command is an alias for reset command.')
        test_parser = self.subparsers.add_parser('test', help='Test to see if you\'ve successfully completed the current level', description='Test to see if you\'ve successfully completed the current level')
        progress_parser = self.subparsers.add_parser('progress', help='Continue to the next level', description='Continue to the next level')
        skills_parser = self.subparsers.add_parser('skills', help='List skills', description='List skills')
        levels_parser = self.subparsers.add_parser('levels', help='List levels', description='List levels in current skill or in other skill if specified')
        load_parser = self.subparsers.add_parser('load', help='Load a specific skill or level', description='Load a specific skill or level')
        commit_parser = self.subparsers.add_parser('commit', help='Quickly create and commit a file', description='Quickly create and commit a file')
        goal_parser = self.subparsers.add_parser('goal', help='Show a description of the current goal', description='Show a description of the current goal')
        show_tree_parser = self.subparsers.add_parser('show-tree', help='Show the current state of the branching tree', description='Show the current state of the branching tree')
        contrib_parser = self.subparsers.add_parser('contributors', help='Show all the contributors of the project', description='Show all the contributors of the project')

        help_parser.add_argument('command_name', metavar='<command>', nargs='?')

        start_parser.add_argument('--force', action='store_true')

        levels_parser.add_argument('skill_name', metavar='skill', nargs='?')

        load_parser.add_argument('skill_name', metavar='skill', help='Skill to load')
        load_parser.add_argument('level_name', metavar='level', nargs='?', help='Level to load')

        commit_parser.add_argument('file', nargs='?')

        self.command_dict = {
            'help': self.handle_help,
            'start': self.handle_start,
            'status': self.handle_status,
            'instructions': self.handle_instructions,
            'goal': self.handle_goal,
            'reset': self.handle_reset,
            'reload': self.handle_reset,
            'test': self.handle_test,
            'progress': self.handle_progress,
            'skills': self.handle_skills,
            'levels': self.handle_levels,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'show-tree': self.handle_show_tree,
            'contributors': self.handle_contrib,
        }

    def is_initialized(self):
        return self.file_operator is not None

    def assert_initialized(self, skip_level_check=False):
        if not self.is_initialized():
            raise InitializationError("Git gud has not been initialized. Use \"git gud start\" to initialize")

        if not skip_level_check:
            try:
                self.file_operator.get_level()
            except KeyError:
                level_name = self.file_operator.read_level_file()
                raise InitializationError("Currently loaded level does not exist: \"{}\"".format(level_name))

    def load_level(self, level):
        level.setup(self.file_operator)
        self.file_operator.write_level(level)
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
            if not self.file_operator:
                self.file_operator = Operator(os.getcwd(), initialize_repo=False)

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
            level_file.write(all_skills[0][0].full_name())

        python_exec = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

        for git_hook_name, module_hook_name in all_hooks:
            with open(os.path.join(self.file_operator.hooks_path, git_hook_name), 'w+') as hook_file:
                hook_file.write('#!/bin/sh' + os.linesep)
                hook_file.write('cat - | '
                                + python_exec + ' -m gitgud.hooks.' + module_hook_name + ' "$@"' + os.linesep)
                hook_file.write('exit 0' + os.linesep)

        print('Git Gud successfully setup in {}'.format(os.getcwd()))

        self.file_operator.get_level().setup(self.file_operator)
        show_tree()

    def handle_status(self, args):
        self.assert_initialized()
        level_name = self.file_operator.get_level().full_name()
        print("Currently on level: \"{}\"".format(level_name))

    def handle_instructions(self, args):
        self.assert_initialized()
        self.file_operator.get_level().instructions()

    def handle_goal(self, args):
        self.assert_initialized()
        self.file_operator.get_level().goal()

    def handle_reset(self, args):
        self.assert_initialized()

        level = self.file_operator.get_level()
        print("Resetting...")
        level.setup(self.file_operator)
        show_tree()

    def handle_test(self, args):
        self.assert_initialized()
        level = self.file_operator.get_level()
        level.test(self.file_operator)

    def handle_progress(self, args):
        self.assert_initialized()

        print("Progressing to next skill...")
        print()

        level = self.file_operator.get_level()

        next_level = level.next_level
        if next_level is not None:
            self.load_level(next_level)
        else:
            print_all_complete()

    def handle_skills(self, args):
        try:
            cur_skill = self.file_operator.get_level().skill
            print("Currently on skill: \"{}\"".format(cur_skill.name))
            print()
        except KeyError:
            pass
        
        skill_chars = max(len(skill.name) for skill in all_skills)
        skill_format_template = "Skill {{}} - {{:<{}}} :{{:>2}} level{{}}".format(skill_chars)
        level_format_template = "{}    Level {{:>2}} : {{:<3}}".format(" " * (skill_chars))
        for i, skill in enumerate(all_skills):
            # TODO Add description
            # 10 characters for the short IDs. 
            print(skill_format_template.format(i + 1, "\"" + skill.name + "\"", len(skill), ("", "s")[len(skill) > 1]))
            
            for index, level in enumerate(skill):
                # " " * (characters allocated for ID - 6)
                print(level_format_template.format(index + 1, level.name))

    def handle_levels(self, args):
        key_error_flag = False
        if args.skill_name is None:
            try:
                skill = self.file_operator.get_level().skill
            except KeyError:
                skill_name = self.file_operator.read_level_file().split()[0]
                print("Cannot find any levels in skill: \"{}\"".format(skill_name))
                return
        else:
            try:
                skill = all_skills[args.skill_name]
            except KeyError:
                print("There is no skill \"{}\".".format(args.skill_name))
                print("You may run \"git gud skills\" to print all the skills. \n")
                skill = self.file_operator.get_level().skill
                key_error_flag = True
        
        if key_error_flag or args.skill_name is None:
            print("Levels in the current skill \"{}\" : \n".format(skill.name))
        else:
            print("Levels for skill \"{}\" : \n".format(skill.name))

        for index, level in enumerate(skill):
            print(str(index + 1) + ": " + level.name)

    def handle_load(self, args):
        self.assert_initialized(skip_level_check=True)
        
        argset = args.skill_name.split("-")

        if (len(argset) == 2):
            args.skill_name, args.level_name = tuple(argset)
        elif(len(argset) > 2):
            print("You put too many dashes! Use at most one dash when trying to load a level.")
            return
        
        args.skill_name = int(args.skill_name) - 1 if args.skill_name.isnumeric() else args.skill_name
        args.level_name = int(args.level_name) - 1 if (args.level_name is not None and args.level_name.isnumeric()) else args.level_name
        
        if args.skill_name in all_skills or (isinstance(args.skill_name, int) and args.skill_name in range(len(all_skills))):
            skill = all_skills[args.skill_name]
            if args.level_name is not None:
                if args.level_name in all_skills[args.skill_name]  or (isinstance(args.level_name, int) and args.level_name in range(len(all_skills[args.skill_name]))):
                    level = skill[args.level_name]
                    self.load_level(level)
                else:
                    print("Level \"{}\" does not exist".format(args.level_name if not isinstance(args.level_name, int) else args.level_name + 1))
                    print("To view levels/skills, use git gud levels or git gud skills")
            else:
                self.load_level(skill[0])
        else:
            print("Skill \"{}\" does not exist".format(args.skill_name if not isinstance(args.skill_name, int) else args.skill_name + 1))
            print("To view levels/skills, use git gud levels or git gud skills")

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

        commit = self.file_operator.add_and_commit(commit_name)
        print("New Commit: {}".format(commit.hexsha[:7]))

        # Check if the newest commit is greater than the last_commit, if yes, then write

        if int(commit_name) > int(last_commit):
            self.file_operator.write_last_commit(commit_name)

    def handle_show_tree(self, args):
        show_tree()

    def handle_contrib(self, args):
        contrib_website = "https://github.com/bthayer2365/git-gud/graphs/contributors"
        webbrowser.open_new(contrib_website)

    def parse(self):
        args, _ = self.parser.parse_known_args()
        if args.command is None:
            self.parser.print_help()
        else:
            try:
                self.command_dict[args.command](args)
            except InitializationError as error:
                print(error)


if __name__ == '__main__':
    GitGud().parse()
