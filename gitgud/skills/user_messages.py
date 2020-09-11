import subprocess

from gitgud import operations
from . import level_builder
from .util import Skill

user_has_seen_messages = False


def existence_str(condition):
    if condition:
        return "Exists"
    else:
        return "Doesn't exist"


def start_marker():
    return '<' * 7


def end_marker():
    return '=' * 7


def separated(func):
    def new_func(*args, **kwargs):
        global user_has_seen_messages
        if user_has_seen_messages:
            print()
        else:
            user_has_seen_messages = True
        func(*args, **kwargs)
    return new_func


@separated
def cat_file(path):
    print(path.read_text().strip())


@separated
def print_user_message(message):
    print(message)


@separated
def show_level_name(level):
    print('Level: "{}"'.format(level.full_name()))


def print_info(message):
    print("[INFO]: {}".format(message))


def mock_simulate(command):
    print(end_marker(), "Simulating: {}".format(command))


@separated
def simulate_command(command):
    print(start_marker(), "Simulating: {}".format(command))
    subprocess.call(command, shell=True)
    print(end_marker())


def show_tree():
    simulate_command("git log --graph --oneline --all")


@separated
def help():
    print("Type \"git gud explain\" for an explaination of the level")
    print("Type \"git gud test\" to test for level completion")
    print("Type \"git gud help\" for more help")


@separated
def level_complete(level):
    print('Level complete! "git gud load next" to advance to the next level')
    print('Next level is: {}'.format(level.next_level.full_name()))


@separated
def skill_complete(level):
    print("Level complete, you've completed all levels in this skill!")
    print('"git gud load next" to advance to the next skill')
    print("Next skill is: {}".format(level.next_level.skill.name))


@separated
def all_levels_complete():
    print("Wow! You've complete every level, congratulations!")

    print("If you want to keep learning git, why not try contributing"
          " to git-gud by forking the project at "
          "https://github.com/benthayer/git-gud/")

    print("We're always looking for contributions and are more than"
          " happy to accept both pull requests and suggestions!")


@separated
def default_fail():
    print('Level not complete, keep trying. "git gud reset" to start from scratch.')  # noqa: E501


def handle_solution_confirmation(level):
    print('Are you sure you want to view the solution for "{}": "{}"?'.format(level.name, level.skill.name))  # noqa: E501
    print('If so, run `git gud solution --confirm`')


@separated
def handle_load_confirm():
    print("You haven't completed this level yet!")
    print("Run `git gud load next` with --force to load the next level.")


def no_solutions_available():
    print("No solutions available for this level.")


@separated
def default_fail_no_reset():
    print('Level not complete, keep trying.')


def show_skill_tree(items, show_human_names=True, show_code_names=True, expand_skills=False):  # noqa: E501
    middle_entry_bookend = '├──'
    last_entry_bookend = '└──'

    file_operator = operations.get_operator()

    completion = {
        "unvisited": ' ',
        "visited": 'X',
        "partial": 'P',
        "complete": 'O'
    }

    format_string = "{index}. "
    if show_human_names and not show_code_names:
        format_string += "{name}"
    elif show_code_names and not show_human_names:
        format_string += "{code}"
    else:
        format_string += "{name} ({code})"

    def display_entry(index, human_name, code_name, indent):
        print(indent + format_string.format(
            index=index, name=human_name, code=code_name))

    if expand_skills:
        new_items = []
        for skill in items:
            assert isinstance(skill, Skill)
            new_items.append(skill)
            for level in skill:
                new_items.append(level)

        items = new_items

    for i, item in enumerate(items):
        if isinstance(item, Skill):
            display_entry(
                item.all_skills.index(item.name),
                human_name=item.readable_name,
                code_name=item.name,
                indent=""
            )
        else:
            assert isinstance(item, level_builder.Level)
            if i + 1 == len(items) or isinstance(items[i+1], Skill):
                indent = last_entry_bookend
            else:
                indent = middle_entry_bookend

            if file_operator:
                indent += completion[item.get_progress()]
            indent += " "

            display_entry(
                item.skill.index(item.name),
                human_name=item.readable_name,
                code_name=item.name,
                indent=indent
            )


def display_tree_content(header, content, show_content=True, file_count=2):
    file_format_str = "  {path} - {content}"

    available_files = list(content.keys())
    # If there are more files than we requested, we want to show that too

    print(header + ":")
    for filepath in available_files:
        file_content = filepath if show_content else existence_str(True)
        print(file_format_str.format(
            path=filepath,
            content=file_content
        ))

    for missing_file_number in range(len(available_files), file_count):
        print(file_format_str.format(
            path=f"File {missing_file_number + 1}",
            content="Missing"
        ))


def display_commit_content(show_branches=True, show_content=True, file_count=2):  # noqa: E501
    file_operator = operations.get_operator()
    referred_by = target_branch_str()

    commit_format_str = "{message}"
    if show_branches:
        commit_format_str += " ({branches})"
    commit_format_str += ":"

    for commit in file_operator.get_all_commits():
        if commit.hexsha in referred_by and show_branches:
            branches = referred_by[commit.hexsha]
        else:
            branches = ""
        header = commit_format_str.format(
            message=commit.message,
            branches=branches
        )
        display_tree_content(
            header,
            file_operator.get_commit_content(commit),
            file_count=2
        )


def target_branch_str():
    file_operator = operations.get_operator()
    referred_by = file_operator.commits_targeted_by()
    for target in referred_by:
        referred_by[target] = ", ".join(referred_by[target])
    return referred_by
