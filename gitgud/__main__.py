import webbrowser
from pathlib import Path

import argparse

import gitgud
from gitgud import operations
from gitgud.skills import all_skills
from gitgud.skills.user_messages import all_levels_complete
from gitgud.skills.user_messages import show_tree
from gitgud.skills.user_messages import handle_solution_confirmation
from gitgud.skills.user_messages import show_skill_tree


class InitializationError(Exception):
    pass


class GitGud:
    def __init__(self):
        # Only gets operator if Git Gud has been initialized
        self.parser = argparse.ArgumentParser(prog='git gud')
        self.parser.add_argument(
                '--version',
                action='version',
                version='%(prog)s ' + gitgud.__version__)

        load_description = '\n'.join([
            "Load a specific skill or level. This command can be used in several ways.",  # noqa: E501
            "\n",
            "============Basic Usage============",
            "\n",
            "These commands are the simplest commands to load a level on a certain skill, and are identical in functionality:",  # noqa: E501
            "\n",
            "   git gud load <skill> <level>",
            "   git gud load <skill>-<level>",
            "\n",
            "<skill> and <level> could either be the name of the skill/level or the number of the skill/level.",  # noqa: E501
            "Running `git gud levels --all --short` will help you find the number and name associated with each skill/level.",  # noqa: E501
            "\n",
            "Here are example uses which load the same level:",
            "\n",
            "   git gud load basics-2",
            "   git gud load 1 branching",
            "\n",
            "============Additional Commands============",
            "\n",
            "`git gud load` supports additional shortcut commands to ease level navigation.",  # noqa: E501
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
            "NOTE: <level> MUST be a number in order for this command to work.",  # noqa: E501
            "\n",
            "   git gud load -<level>",
            "\n",
        ])

        show_description = "\n".join([
            "Helper command to show certain information.",
            "\n",
            "Subcommands:",
            "  <command>",
            "    tree\tShow the current state of the branching tree"
        ])

        self.subparsers = self.parser.add_subparsers(
                title='Subcommands',
                metavar='<command>',
                dest='command'
        )

        self.subparsers.add_parser(
                'status',
                help='Print out the name of the current level',
                description='Print out the name of the current level')
        self.subparsers.add_parser(
                'explain',
                help='Show the explain for the current level',
                description='Show the explain for the current level')
        self.subparsers.add_parser(
                'goal',
                help='Concisely show what needs to be done to complete the level.',  # noqa: E501
                description='Concisely show what needs to be done to complete the level.')  # noqa: E501
        self.subparsers.add_parser(
                'reset',
                help='Reset the current level',
                description='Reset the current level')
        self.subparsers.add_parser(
                'reload',
                help='Alias for reset',
                description='Reset the current level. Reload command is an alias for reset command.')  # noqa: E501
        self.subparsers.add_parser(
                'test',
                help="Test to see if you've successfully completed the current level",  # noqa: E501
                description="Test to see if you've successfully completed the current level")  # noqa: E501
        self.subparsers.add_parser(
                'level',
                help='Display current level',
                description='Display the currently loaded level')
        self.subparsers.add_parser(
                'goal',
                help='Show a description of the current goal',
                description='Show a description of the current goal')
        self.subparsers.add_parser(
                'contributors',
                help='Show project contributors webpage',
                description='Show all the contributors of the project')
        self.subparsers.add_parser(
                'issues',
                help='Show project issues webpage',
                description="Show all the issues for the project")

        help_parser = self.subparsers.add_parser(
                'help',
                help='Show help for commands',
                description='Show help for commands'
        )
        help_parser.add_argument(
                'command_name',
                metavar='cmd',
                help="Command to get help on", nargs='?'
        )

        solution_parser = self.subparsers.add_parser(
                'solution',
                help='Show solution for the given level',
                description='Show the solution for the given level'
        )
        solution_parser.add_argument('--confirm', action='store_true')

        init_parser = self.subparsers.add_parser(
                'init',
                help='Init Git Gud and load first level',
                description='Initialize the direcotry with a git repository and load the first level of Git Gud.'  # noqa: E501
        )
        init_parser.add_argument('--force', action='store_true')
        init_parser.add_argument('--prettyplease', action='store_true')

        load_parser = self.subparsers.add_parser(
                'load',
                help='Load a specific skill or level',
                description=load_description,
                formatter_class=argparse.RawDescriptionHelpFormatter)
        load_parser.add_argument(
                'skill_name',
                metavar='skill',
                help='Skill to load')
        load_parser.add_argument(
                'level_name',
                metavar='level',
                nargs='?',
                help='Level to load')

        skills_parser = self.subparsers.add_parser(
                'skills',
                help='List skills',
                description='List skills')
        skills_parser.add_argument('--short', dest='opt_short', action='store_true', help="Prints with the short name of skills usable with `git gud load`.")  # noqa: E501

        levels_parser = self.subparsers.add_parser(
                'levels',
                help='List levels in a skill',
                description='List the levels in the specified skill or in the current skill if Git Gud has been initialized and no skill is provided. To see levels in all skills, use `git gud levels --all`.')  # noqa: E501
        levels_parser.add_argument('skill_name', metavar='skill', nargs='?')
        levels_parser.add_argument('--all', dest='opt_all', action='store_true', help="Prints all available skills with levels.")  # noqa: E501
        levels_parser.add_argument('--short', dest='opt_short', action='store_true', help="Prints with the short name of skills/levels usable with `git gud load`.")  # noqa: E501

        commit_parser = self.subparsers.add_parser(
                'commit',
                help='Quickly create and commit a file',
                description='Quickly create and commit a file')
        commit_parser.add_argument('file', nargs='?')

        show_parser = self.subparsers.add_parser(
                'show',
                description=show_description,
                formatter_class=argparse.RawDescriptionHelpFormatter)
        show_parser.add_argument(
                'cmd',
                metavar='cmd',
                help='Command to show information',
                nargs='?')

        self.command_dict = {
            'help': self.handle_help,
            'init': self.handle_init,
            'status': self.handle_status,
            'explain': self.handle_explain,
            'goal': self.handle_goal,
            'reset': self.handle_reset,
            'reload': self.handle_reset,
            'test': self.handle_test,
            'level': self.handle_level,
            'skills': self.handle_skills,
            'levels': self.handle_levels,
            'load': self.handle_load,
            'commit': self.handle_commit,
            'show-tree': self.handle_show_tree,
            'show': self.handle_show,
            'contributors': self.handle_contrib,
            'issues': self.handle_issues,
            'solution': self.handle_solution
        }

    def is_initialized(self):
        return operations.get_operator() is not None

    def assert_initialized(self, skip_level_check=False):
        if not self.is_initialized():
            raise InitializationError('Git gud has not been initialized. Use "git gud init" to initialize')  # noqa: E501

        if not skip_level_check:
            try:
                self.get_level()
            except KeyError:
                level_name = operations.get_operator().read_level_file()
                raise InitializationError(
                        'Currently loaded level does not exist: "{}"'
                        .format(level_name))

    def load_level(self, level):
        self.assert_initialized(skip_level_check=True)
        file_operator = operations.get_operator()
        file_operator.clear_tracked_commits()
        level.setup()
        file_operator.write_level(level)

    def get_level(self):
        skill_name, level_name = operations.get_operator().read_level_file().split()  # noqa: E501
        return all_skills[skill_name][level_name]

    def handle_help(self, args):
        if args.command_name is None:
            self.parser.print_help()
        else:
            try:
                self.subparsers.choices[args.command_name].print_help()
            except KeyError:
                print('No such command exists: "{}"'
                      .format(args.command_name))
                print()
                self.parser.print_help()

    def handle_init(self, args):
        # Make sure it's safe to initialize

        file_operator = operations.get_operator()
        if file_operator:
            if not args.force:
                print('Repo {} already initialized for Git Gud.'
                      .format(file_operator.path))
                print('Use --force to initialize {}.'.format(Path.cwd()))
                if file_operator.path != Path.cwd():
                    print('{} will be left as is.'.format(file_operator.gg_path))  # noqa: E501
                return
            else:
                print('Force initializing Git Gud.')
        elif len(list(Path.cwd().iterdir())) != 0:
            if not (args.force and args.prettyplease):
                print('Current directory is nonempty. Initializing will delete all files.')  # noqa: E501
                print('Use --force --prettyplease to force initialize here.')
                return
            else:
                print('Deleting all files.')
                print('Initializing Git Gud.')

        file_operator = operations.get_operator(Path.cwd())

        assert file_operator is not None

        file_operator.init_gg()

        print()

        self.load_level(all_skills["0"]["1"])

    def handle_status(self, args):
        if self.is_initialized():
            try:
                level = self.get_level()
                level.status()
            except KeyError:
                level_name = operations.get_operator().read_level_file()
                print('Currently on unregistered level: "{}"'
                      .format(level_name))
        else:
            print("Git Gud not initialized.")
            print('Initialize using "git gud init"')

    def handle_explain(self, args):
        self.assert_initialized()
        self.get_level().explain()

    def handle_goal(self, args):
        self.assert_initialized()
        self.get_level().goal()

    def handle_reset(self, args):
        self.assert_initialized()

        level = self.get_level()
        self.load_level(level)

    def handle_test(self, args):
        self.assert_initialized()
        level = self.get_level()
        level.test()

    def handle_solution(self, args):
        self.assert_initialized()
        current_level = self.get_level()
        if not args.confirm and \
                not current_level.has_ever_been_completed():
            handle_solution_confirmation(current_level)
        else:
            current_level.solution()

    def handle_level(self, args):
        level = self.get_level()
        skill = level.skill
        show_skill_tree(
                [skill, level],
                expand_skills=False)

    def handle_skills(self, args):
        print("All skills:")
        print()
        show_skill_tree(
            [skill for skill in all_skills],
            expand_skills=False,
            show_human_names=not args.opt_short
        )

    def handle_levels(self, args):
        if args.opt_all:
            skills_to_show = [skill for skill in all_skills]
            print("All levels and skills:")
        else:
            # Only show levels in one skill
            if args.skill_name:
                try:
                    skills_to_show = [all_skills[args.skill_name]]
                    print('Levels in skill "{}" :'.format(args.skill_name))
                except KeyError:
                    print('There is no skill "{}".'.format(args.skill_name))
                    print('You may run "git gud levels --all" or "git gud levels --skills" to print all the skills.')  # noqa: E501
                    return
            elif self.is_initialized():
                current_skill = self.get_level().skill
                skills_to_show = [current_skill]
                print('Levels in the current skill "{}" :'.format(current_skill.name))  # noqa: E501
            else:
                self.subparsers.choices['levels'].print_help()
                return

        print()
        show_skill_tree(
            skills_to_show,
            expand_skills=True,
            show_human_names=not args.opt_short
        )
        print()
        print("Load a level with `git gud load`")

    def handle_load(self, args):
        self.assert_initialized(skip_level_check=True)

        argskillset = args.skill_name.split("-", 1)

        # Set up args.level_name and args.skill_name
        if args.level_name:
            if args.skill_name == "-":
                # Replace the dash with the current skill's name.
                args.skill_name = self.get_level().skill.name
        else:
            if len(argskillset) == 2:
                args.skill_name, args.level_name = tuple(argskillset)
            else:
                args.skill_name, args.level_name = argskillset[0], None

        skill_to_load = self.get_level().skill.name
        if args.skill_name:
            if args.skill_name.lower() in {"next", "prev", "previous"}:
                query = args.skill_name.lower()
                level = self.get_level()

                if query == "next":
                    level_to_load = level.next_level
                else:
                    query = "previous"
                    level_to_load = level.prev_level

                if level_to_load is not None:
                    self.load_level(level_to_load)
                else:
                    if query == "next":
                        all_levels_complete()
                    else:
                        print('Already on the first level. To reload the level, use "git gud reload".')  # noqa: E501
                    print('\nTo view levels/skills, use "git gud levels --all"')  # noqa: E501
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
                print('\nTo view levels/skills, use "git gud levels --all"')  # noqa: E501
        else:
            print('Skill "{}" does not exist'.format(args.skill_name))
            print('\nTo view levels/skills, use "git gud levels --all"')  # noqa: E501

    def handle_commit(self, args):
        self.assert_initialized()
        file_operator = operations.get_operator()
        last_commit = file_operator.get_last_commit()
        commit_name = str(int(last_commit) + 1)

        if args.file is not None:
            try:
                int(args.file)
                commit_name = args.file
            except ValueError:
                pass

        commit = file_operator.add_and_commit(commit_name, silent=False)
        file_operator.track_commit(commit_name, commit.hexsha)

        # Next "git gud commit" name
        if int(commit_name) > int(last_commit):
            file_operator.write_last_commit(commit_name)

    def handle_show(self, args):
        if args.cmd == "tree":
            show_tree()
        else:
            print('Error: `git gud show` takes specific arguments. Type `git gud help show` for more information.')  # noqa: E501

    def handle_show_tree(self, args):
        show_tree()

    def handle_contrib(self, args):
        contrib_website = "https://github.com/benthayer/git-gud/graphs/" \
            "contributors"
        webbrowser.open_new(contrib_website)

    def handle_issues(self, args):
        issues_website = "https://github.com/benthayer/git-gud/issues"
        webbrowser.open_new(issues_website)

    def parse(self):
        args, _ = self.parser.parse_known_args()
        if args.command is None:
            if operations.get_operator() is None:
                print('Currently in an uninitialized directory.')
                print('Get started by running "git gud init" in an empty directory!')  # noqa: E501
            else:
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
