import webbrowser
from pathlib import Path

import sys
import argparse

from gitgud import __version__, InitializationError
from gitgud.util.operations import Operator, get_operator
from gitgud.skills import all_skills

from gitgud.user_messages import force_initializing
from gitgud.user_messages import cant_init_repo_not_empty
from gitgud.user_messages import deleting_and_initializing
from gitgud.user_messages import all_levels_complete
from gitgud.user_messages import show_tree
from gitgud.user_messages import handle_load_confirm
from gitgud.user_messages import rerun_with_confirm_for_solution
from gitgud.user_messages import show_skill_tree
from gitgud.user_messages.stateful import repo_already_initialized


def link_command(parser):
    def set_default(handler):
        parser.set_defaults(func=lambda gg, args: handler(gg, args))
        return handler
    return set_default


class GitGud:
    parser = argparse.ArgumentParser(
        prog='git gud',
        description='A game to teach Git!')
    parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + __version__)

    show_description = "\n".join([
        "Helper command to show certain information.",
        "\n",
        "Subcommands:",
        "  <command>",
        "    tree\tShow the current state of the branching tree"
    ])

    subparsers = parser.add_subparsers(
            title='Subcommands',
            metavar='<command>',
            dest='command'
    )

    def __init__(self):
        self.aliases = {
            'h': 'help',
            'i': 'issues',
            's': 'status',
            'e': 'explain',
            'g': 'goal',
            't': 'test',
            'l': 'load',
            'c': 'commit',
            'r': 'reset',
            'reload': 'reset',
        }

        self.parser.epilog = "The following aliases exist: "
        for alias in self.aliases:
            self.parser.epilog += "'{}' -> '{}', " \
                    .format(alias, self.aliases[alias])
        self.parser.epilog = self.parser.epilog[:-2]

    def is_initialized(self):
        return get_operator() is not None

    def assert_initialized(self):
        if not self.is_initialized():
            raise InitializationError('Git Gud has not been initialized. Use "git gud init" to initialize.')  # noqa: E501

    def load_level(self, level):
        self.assert_initialized()
        file_operator = get_operator()
        file_operator.clear_tracked_commits()
        level.setup()
        file_operator.write_level(level)

    help_parser = subparsers.add_parser(
            'help',
            help='Show help for commands',
            description='Show help for commands'
    )
    help_parser.add_argument(
            'command_name',
            metavar='cmd',
            help="Command to get help on", nargs='?'
    )

    @link_command(help_parser)
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

    init_parser = subparsers.add_parser(
            'init',
            help='Init Git Gud and load first level',
            description='Initialize the directory with a git repository and load the first level of Git Gud.'  # noqa: E501
    )
    init_parser.add_argument('--force', action='store_true')
    init_parser.add_argument('--prettyplease', action='store_true')

    @link_command(init_parser)
    def handle_init(self, args):
        # Make sure it's safe to initialize

        file_operator = get_operator()
        if file_operator:
            if not args.force:
                repo_already_initialized()
                return
            else:
                force_initializing()
        elif len(list(Path.cwd().iterdir())) != 0:
            if not (args.force and args.prettyplease):
                cant_init_repo_not_empty()
                return
            else:
                deleting_and_initializing()

        file_operator = Operator(Path.cwd())
        file_operator.init_gg()

        self.load_level(all_skills["0"]["1"])

    status_parser = subparsers.add_parser(
            'status',
            help='Print out the name of the current level',
            description='Print out the name of the current level'
    )

    @link_command(status_parser)
    def handle_status(self, args):
        self.assert_initialized()
        get_operator().get_level().status()

    explain_parser = subparsers.add_parser(
            'explain',
            help='Show the explain for the current level',
            description='Show the explain for the current level'
    )

    @link_command(explain_parser)
    def handle_explain(self, args):
        self.assert_initialized()
        get_operator().get_level().explain()

    goal_parser = subparsers.add_parser(
            'goal',
            help='Show a description of the current goal',
            description='Show a description of the current goal'
    )

    @link_command(goal_parser)
    def handle_goal(self, args):
        self.assert_initialized()
        get_operator().get_level().goal()

    reset_parser = subparsers.add_parser(
            'reset',
            help='Reset the current level',
            description='Reset the current level'
    )

    @link_command(reset_parser)
    def handle_reset(self, args):
        self.assert_initialized()

        file_operator = get_operator()

        file_operator.update_level_completion()

        level = file_operator.get_level()
        self.load_level(level)

    test_parser = subparsers.add_parser(
            'test',
            help="Test to see if you've successfully completed the current level",  # noqa: E501
            description="Test to see if you've successfully completed the current level"  # noqa: E501
    )

    @link_command(test_parser)
    def handle_test(self, args):
        self.assert_initialized()
        get_operator().get_level().test()

    solution_parser = subparsers.add_parser(
            'solution',
            help='Show solution for the given level',
            description='Show the solution for the given level'
    )
    solution_parser.add_argument('--confirm', action='store_true')

    @link_command(solution_parser)
    def handle_solution(self, args):
        self.assert_initialized()
        current_level = get_operator().get_level()
        if not args.confirm and \
                not current_level.has_ever_been_completed():
            rerun_with_confirm_for_solution(current_level)
        else:
            current_level.solution()

    level_parser = subparsers.add_parser(
            'level',
            help='Display current level',
            description='Display the currently loaded level'
    )

    @link_command(level_parser)
    def handle_level(self, args):
        self.assert_initialized()
        level = get_operator().get_level()
        skill = level.skill
        show_skill_tree(
                [skill, level],
                True,
                expand_skills=False)

    skills_parser = subparsers.add_parser(
            'skills',
            help='List skills',
            description='List skills')
    skills_parser.add_argument('--short', dest='opt_short', action='store_true', help="Prints with the short name of skills usable with `git gud load`.")  # noqa: E501

    @link_command(skills_parser)
    def handle_skills(self, args):
        print("All skills:")
        print()
        show_skill_tree(
            [skill for skill in all_skills],
            bool(get_operator()),
            expand_skills=False,
            show_human_names=not args.opt_short
        )

    levels_parser = subparsers.add_parser(
            'levels',
            help='List levels in a skill',
            description='List the levels in the specified skill or in the current skill if Git Gud has been initialized and no skill is provided. To see levels in all skills, use `git gud levels --all`.')  # noqa: E501
    levels_parser.add_argument(
            'skill_name',
            metavar='skill',
            nargs='?')
    levels_parser.add_argument(
            '-a',
            '--all',
            dest='opt_all',
            action='store_true',
            help="Prints all available skills with levels.")
    levels_parser.add_argument(
            '--short',
            dest='opt_short',
            action='store_true',
            help="Prints with the short name of skills/levels usable with `git gud load`.")  # noqa: E501

    @link_command(levels_parser)
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
                current_skill = get_operator().get_level().skill
                skills_to_show = [current_skill]
                print('Levels in the current skill "{}" :'.format(current_skill.name))  # noqa: E501
            else:
                self.subparsers.choices['levels'].print_help()
                return

        print()
        show_skill_tree(
            skills_to_show,
            bool(get_operator()),
            expand_skills=True,
            show_human_names=not args.opt_short
        )
        print()
        print("Load a level with `git gud load`")

    def load_level_by_direction(self, load_direction, force):
        if load_direction == "prev":
            load_direction = "previous"

        try:
            level = get_operator().get_level()
        except InitializationError as e:
            print(e)
            print(f"Cannot load {load_direction} level.")
            return

        if load_direction == "next":
            if level.has_ever_been_completed() or force:
                level_to_load = level.next_level
            else:
                handle_load_confirm()
                return
        else:
            level_to_load = level.prev_level

        if level_to_load is not None:
            self.load_level(level_to_load)
        else:
            if load_direction == "next":
                all_levels_complete()
            else:
                print('Already on the first level. To reload the level, use "git gud reload".')  # noqa: E501
            print('\nTo view levels/skills, use "git gud levels --all"')  # noqa: E501

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

    load_parser = subparsers.add_parser(
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
    load_parser.add_argument('--force', action="store_true")

    @link_command(load_parser)
    def handle_load(self, args):
        self.assert_initialized()
        args.skill_name = args.skill_name.lower()
        if args.level_name:
            args.level_name = args.level_name.lower()

        get_operator().update_level_completion()

        if args.skill_name in {"next", "prev", "previous"}:
            self.load_level_by_direction(args.skill_name, args.force)
            return

        # No matter what, the dash separates the skill and level
        if '-' in args.skill_name:
            identifier = args.skill_name + (args.level_name or '')
        else:
            identifier = args.skill_name + '-' + (args.level_name or '')
        if identifier.count('-') != 1:
            print("Load formula must not contain more than one dash.")
            return

        args.skill_name, args.level_name = identifier.split('-')

        if not args.skill_name:
            args.skill_name, loaded_level_name = get_operator() \
                    .get_level_identifier()
            print("Inferring skill from currently loaded level: {} {}"
                  .format(args.skill_name, loaded_level_name))
        if not args.level_name:
            args.level_name = '1'

        # Skill doesn't exist
        if args.skill_name not in all_skills.keys():
            print('Skill "{}" does not exist'.format(args.skill_name))
            print('\nTo view levels/skills, use "git gud levels --all"')
            return

        # Level doesn't exist
        skill = all_skills[args.skill_name]
        if args.level_name not in skill.keys():
            print('Level "{}" does not exist.'.format(args.level_name))
            print('\nTo view levels/skills, use "git gud levels --all"')
            return

        level = skill[args.level_name]
        self.load_level(level)

    commit_parser = subparsers.add_parser(
            'commit',
            help='Quickly create and commit a file',
            description='Quickly create and commit a file')
    commit_parser.add_argument('file', nargs='?')

    @link_command(commit_parser)
    def handle_commit(self, args):
        self.assert_initialized()
        file_operator = get_operator()
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

    show_parser = subparsers.add_parser(
            'show',
            description=show_description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    show_parser.add_argument(
            'cmd',
            metavar='cmd',
            help='Command to show information',
            nargs='?')

    @link_command(show_parser)
    def handle_show(self, args):
        if args.cmd == "tree":
            show_tree()
        else:
            print('Error: `git gud show` takes specific arguments. Type `git gud help show` for more information.')  # noqa: E501

    def handle_show_tree(self, args):
        show_tree()

    contributors_parser = subparsers.add_parser(
            'contributors',
            help='Show project contributors webpage',
            description='Show all the contributors of the project'
    )

    @link_command(contributors_parser)
    def handle_contributors(self, args):
        contrib_website = "https://github.com/benthayer/git-gud/graphs/" \
            "contributors"
        webbrowser.open_new(contrib_website)

    issues_parser = subparsers.add_parser(
            'issues',
            help='Show project issues webpage',
            description="Show all the issues for the project"
    )

    @link_command(issues_parser)
    def handle_issues(self, args):
        issues_website = "https://github.com/benthayer/git-gud/issues"
        webbrowser.open_new(issues_website)

    debug_parser = subparsers.add_parser(
            'debug',
            description='Debug git-gud with necessary imports set up.'
    )

    @link_command(debug_parser)
    def handle_debug(self, args):
        import readline  # noqa: F401
        import code
        variables = globals()

        file_operator = get_operator()
        variables['file_operator'] = file_operator
        variables['op'] = file_operator

        shell = code.InteractiveConsole(variables)
        shell.interact(
            banner="\n".join([
                "You are now in the Python interpreter invoked by `git gud debug`.",  # noqa: E501
                "Your current path is " + str(Path.cwd()),
                "To exit, type exit()"
            ])
        )

    def parse(self):
        if len(sys.argv) >= 2 and sys.argv[1] in self.aliases:
            sys.argv[1] = self.aliases[sys.argv[1]]

        args, _ = self.parser.parse_known_args(sys.argv[1:])

        if args.command is None:
            if get_operator() is None:
                print('Currently in an uninitialized directory.')
                print('Get started by running "git gud init" (without quotes) in an empty directory!')  # noqa: E501
                if len(list(Path.cwd().iterdir())) != 0:
                    print('Current directory is not empty.')
                else:
                    print('Current directory is empty.')
            else:
                self.parser.print_help()
        else:
            try:
                args = self.parser.parse_args()
                args.func(self, args)
            except InitializationError as error:
                print(error)


def main():
    GitGud().parse()


if __name__ == '__main__':
    main()
