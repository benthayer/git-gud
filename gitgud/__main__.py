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


def show_tree():
    print("Simulating: git log --graph --oneline --all ")
    subprocess.call(["git", "log", "--graph", "--oneline", "--all"])


class InitializationError(Exception):
    pass


class GitGud:
    def __init__(self):
        self.file_operator = get_operator()  # Only gets operator if Git Gud has been initialized

        self.parser = argparse.ArgumentParser(prog='git gud')

        load_description = '\n'.join([
            "Load a specific skill or level. This command can be used in several ways.",
            "\n",
            "============Basic Usage============",
            "\n",
            "These commands are the simplest commands to load a level on a certain skill, and are identical in functionality:",
            "\n",
            "   git gud load <skill> <level>",
            "   git gud load <skill>-<level>",
            "\n",
            "<skill> and <level> could either be the name of the skill/level or the number of the skill/level.",
            "Running `git gud skills` will help you find the number and name associated with each skill/level.",
            "\n",
            "Here are example uses which load the same level:",
            "\n",
            "   git gud load basics-2",
            "   git gud load 1 branching",
            "\n",
            "============Additional Commands============",
            "\n",
            "`git gud load` supports additional shortcut commands to ease level navigation.",
            "\n",
            "======Loading the first level on a skill======",
            "\n",
            "This command loads the first level on the specified skill:",
            "\n",
            "   git gud load <skill>",
            "\n",
            "======Loading a level on the current skill======",
            "\n",
            "This command loads the specified level of the current skill.",
            "NOTE: <level> MUST be a number in order for this command to work.",
            "\n",
            "   git gud load -<level>",
            "\n",
        ])
        self.subparsers = self.parser.add_subparsers(title='Subcommands', metavar='<command>', dest='command')

        help_parser = self.subparsers.add_parser('help', help='Show help for commands', description='Show help for commands')
        init_parser = self.subparsers.add_parser('init', help='Init Git Gud and load first level', description='Initialize the direcotry with a git repository and load the first level of Git Gud.')
        status_parser = self.subparsers.add_parser('status', help='Print out the name of the current level', description='Print out the name of the current level')
        instructions_parser = self.subparsers.add_parser('instructions', help='Show the instructions for the current level', description='Show the instructions for the current level')
        goal_parser = self.subparsers.add_parser('goal', help='Concisely show what needs to be done to complete the level.', description='Concisely show what needs to be done to complete the level.')
        reset_parser = self.subparsers.add_parser('reset', help='Reset the current level', description='Reset the current level')
        reload_parser = self.subparsers.add_parser('reload', help='Alias for reset', description='Reset the current level. Reload command is an alias for reset command.')
        test_parser = self.subparsers.add_parser('test', help="Test to see if you've successfully completed the current level", description="Test to see if you've successfully completed the current level")
        skills_parser = self.subparsers.add_parser('skills', help='List skills', description='List skills')
        levels_parser = self.subparsers.add_parser('levels', help='List levels in a skill', description='List the levels in the specified skill or in the current skill if Git Gud has been initialized and no skill is provided.')
        load_parser = self.subparsers.add_parser('load', help='Load a specific skill or level', description=load_description, formatter_class=argparse.RawDescriptionHelpFormatter)
        commit_parser = self.subparsers.add_parser('commit', help='Quickly create and commit a file', description='Quickly create and commit a file')
        goal_parser = self.subparsers.add_parser('goal', help='Show a description of the current goal', description='Show a description of the current goal')
        show_tree_parser = self.subparsers.add_parser('show-tree', help='Show the current state of the branching tree', description='Show the current state of the branching tree')
        contrib_parser = self.subparsers.add_parser('contributors', help='Show project contributors webpage', description='Show all the contributors of the project')
        issues_parser = self.subparsers.add_parser('issues', help='Show project issues webpage', description="Show all the issues for the project")
        
        help_parser.add_argument('command_name', metavar='<command>', nargs='?')

        init_parser.add_argument('--force', action='store_true')

        levels_parser.add_argument('skill_name', metavar='skill', nargs='?')

        load_parser.add_argument('skill_name', metavar='skill', help='Skill to load')
        load_parser.add_argument('level_name', metavar='level', nargs='?', help='Level to load')

        commit_parser.add_argument('file', nargs='?')

        self.command_dict = {
            'help': self.handle_help,
            'init': self.handle_init,
            'status': self.handle_status,
            'instructions': self.handle_instructions,
            'goal': self.handle_goal,
            'reset': self.handle_reset,
            'reload': self.handle_reset,
            'test': self.handle_test,
            'skills': self.handle_skills,
            'levels': self.handle_levels,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'show-tree': self.handle_show_tree,
            'contributors': self.handle_contrib,
            'issues': self.handle_issues    
        }

    def is_initialized(self):
        return self.file_operator is not None

    def assert_initialized(self, skip_level_check=False):
        if not self.is_initialized():
            raise InitializationError('Git gud has not been initialized. Use "git gud init" to initialize')

        if not skip_level_check:
            try:
                self.file_operator.get_level()
            except KeyError:
                level_name = self.file_operator.read_level_file()
                raise InitializationError('Currently loaded level does not exist: "{}"'.format(level_name))

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
                print('No such command exists: "{}"\n'.format(args.command_name))
                self.parser.print_help()

    def handle_init(self, args):
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

        python_exec = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

        for git_hook_name, module_hook_name in all_hooks:
            path = os.path.join(self.file_operator.hooks_path, git_hook_name)
            if (git_hook_name == 'commit-msg'):
                pipeline = 'cat - |'
                passargs =' "$@"'
            else:
                pipeline = ''
                passargs = ''
                
            with open(path, 'w+') as hook_file:
                hook_file.write('#!/bin/sh' + os.linesep)
                hook_file.write(pipeline + python_exec + ' -m gitgud.hooks.' + module_hook_name + passargs + os.linesep)
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
        print('Welcome to Git Gud!')
        print()

        self.load_level(all_skills["1"]["1"])

    def handle_status(self, args):
        if self.is_initialized():
            try:
                level = self.file_operator.get_level()
                print('Currently on level: "{}"'.format(level.full_name()))
            except KeyError:
                level_name = self.file_operator.read_level_file()
                print('Currently on unregistered level: "{}"'.format(level_name))
        else:
            print("Git gud not initialized.")
            print('Initialize using "git gud init"')

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
        self.load_level(level)

    def handle_test(self, args):
        self.assert_initialized()
        level = self.file_operator.get_level()
        level.test(self.file_operator)

    def handle_skills(self, args):
        if self.is_initialized():
            try:
                cur_skill = self.file_operator.get_level().skill
                print('Currently on skill: "{}"'.format(cur_skill.name))
                print()
            except KeyError:
                pass
        
        skill_chars = max(len(skill.name) for skill in all_skills)
        skill_format_template = 'Skill {{}} - "{{:<{}}}" :{{:>2}} level{{}}'.format(skill_chars)
        level_format_template = "    Level {:>2} : {:<3}"
        
        for i, skill in enumerate(all_skills):
            # TODO Add description
            print(skill_format_template.format(i + 1, skill.name, len(skill), ("", "s")[len(skill) > 1]))

            for index, level in enumerate(skill):
                print(level_format_template.format(index + 1, level.name))
        
        print("\nLoad a level with `git gud load`")
        
    def handle_levels(self, args):
        key_error_flag = False
        if args.skill_name is None:
            if self.file_operator is None:
                self.subparsers.choices['levels'].print_help()
                return
            try:
                skill = self.file_operator.get_level().skill
            except KeyError:
                skill_name = self.file_operator.read_level_file().split()[0]
                print('Cannot find any levels in skill: "{}"'.format(skill_name))
                return
        else:
            try:
                skill = all_skills[args.skill_name]
            except KeyError:
                print('There is no skill "{}".'.format(args.skill_name))
                print('You may run "git gud skills" to print all the skills. \n')
                skill = self.file_operator.get_level().skill
                key_error_flag = True
        
        if key_error_flag or args.skill_name is None:
            print('Levels in the current skill "{}" : \n'.format(skill.name))
        else:
            print('Levels for skill "{}" : \n'.format(skill.name))

        for index, level in enumerate(skill):
            print(str(index + 1) + ": " + level.name)

        print('\nTo see levels in all skills, run "git gud skills".')

    def handle_load(self, args):
        self.assert_initialized(skip_level_check=True)

        argskillset = args.skill_name.split("-", 1)
        
        # Set up args.level_name and args.skill_name
        if args.level_name:
            if args.skill_name is "-":
                # Replace the dash with the current skill's name.
                args.skill_name = self.file_operator.get_level().skill.name
        else:
            if len(argskillset) == 2:   
                args.skill_name, args.level_name = tuple(argskillset)
            else:
                args.skill_name, args.level_name = argskillset[0], None

        skill_to_load = self.file_operator.get_level().skill.name
        if args.skill_name:
            if args.skill_name.lower() in {"next", "prev", "previous"}:
                query = args.skill_name.lower()
                level = self.file_operator.get_level()
                                
                if query == "next":
                    level_to_load = level.next_level
                else:
                    query = "previous"
                    level_to_load = level.prev_level
                
                print("Loading the {} level...\n".format(query))

                if level_to_load is not None:
                    self.load_level(level_to_load)
                else:
                    print('To view levels/skills, use "git gud levels" or "git gud skills"\n')
                    if query == "next":
                        print_all_complete()
                    else:
                        print('Already on the first level. To reload the level, use "git gud reload".')
                return
            else:
                skill_to_load = args.skill_name
        
        level_to_load = '1'
        if args.level_name:
            level_to_load = args.level_name

        if skill_to_load in all_skills.keys():
            skill = all_skills[skill_to_load]
            if level_to_load in skill.keys():
                    level = skill[level_to_load]
                    self.load_level(level)
            else:
                print('Level "{}" does not exist'.format(args.level_name))
                print('To view levels/skills, use "git gud levels" or "git gud skills"\n')
        else:
            print('Skill "{}" does not exist'.format(args.skill_name))
            print('To view levels/skills, use "git gud levels" or "git gud skills"\n')


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

        print('Simulating: Create file "{}"'.format(commit_name))
        print('Simulating: git add {}'.format(commit_name))
        print('Simulating: git commit -m "{}"'.format(commit_name))

        commit = self.file_operator.add_and_commit(commit_name)
        print("New Commit: {}".format(commit.hexsha[:7]))

        # Check if the newest commit is greater than the last_commit, if yes, then write

        if int(commit_name) > int(last_commit):
            self.file_operator.write_last_commit(commit_name)

    def handle_show_tree(self, args):
        show_tree()

    def handle_contrib(self, args):
        contrib_website = "https://github.com/benthayer/git-gud/graphs/contributors"
        webbrowser.open_new(contrib_website)

    def handle_issues(self, args):
        issues_website = "https://github.com/benthayer/git-gud/issues"
        webbrowser.open_new(issues_website)
    
    def parse(self):
        args, _ = self.parser.parse_known_args()
        if args.command is None:
            self.parser.print_help()
        else:
            try:
                self.command_dict[args.command](args)
            except InitializationError as error:
                print(error)


def main():
    GitGud().parse()


if __name__ == '__main__':
    main()
